// netlify/functions/notify-business-submission.js
//
// Recoit un webhook Supabase declenche a chaque nouvelle ligne inseree
// dans la table business_submissions (candidature commerce via le
// formulaire Economya Escape), et envoie un email de notification via
// l'API Resend.
//
// Avant cette fonction, une candidature arrivait en base sans que
// personne ne soit prevenu : il fallait penser a aller consulter
// /admin-business.html de temps en temps. Desormais un email part
// automatiquement des la soumission.
//
// Configuration necessaire (variables d'environnement Netlify) :
//   - RESEND_API_KEY        : cle API Resend (https://resend.com)
//   - NOTIFY_EMAIL_TO       : adresse qui recoit les notifications
//                             (defaut : contact@economya.fr)
//   - NOTIFY_EMAIL_FROM     : adresse d'expedition, doit etre sur un
//                             domaine verifie dans Resend une fois
//                             pret (defaut : onboarding@resend.dev,
//                             qui ne fonctionne que pour envoyer vers
//                             l'adresse du compte Resend lui-meme,
//                             utile pour tester avant verification du
//                             domaine economya.fr).
//   - WEBHOOK_SECRET        : optionnel. Si defini, la requete entrante
//                             doit porter un header
//                             "x-webhook-secret" avec la meme valeur
//                             (a configurer cote Supabase, section
//                             Database Webhooks > HTTP Headers), pour
//                             eviter que n'importe qui puisse declencher
//                             des emails en appelant l'URL de la
//                             fonction directement.
//
// En cas d'erreur (cle manquante, Resend indisponible, etc.), la
// fonction repond simplement par un statut d'erreur : elle ne doit
// jamais faire echouer l'insertion Supabase elle-meme, qui a deja eu
// lieu avant que ce webhook ne soit appele.

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const expectedSecret = process.env.WEBHOOK_SECRET;
  if (expectedSecret) {
    const got = event.headers['x-webhook-secret'] || event.headers['X-Webhook-Secret'];
    if (got !== expectedSecret) {
      return { statusCode: 401, body: 'Unauthorized' };
    }
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error('notify-business-submission: RESEND_API_KEY manquante');
    return { statusCode: 500, body: 'RESEND_API_KEY not configured' };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || '{}');
  } catch (e) {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  // Supabase Database Webhooks envoie { type, table, record, schema, old_record }
  const s = payload.record || payload;
  if (!s || !s.nom_commerce) {
    return { statusCode: 400, body: 'Missing record.nom_commerce' };
  }

  const to = process.env.NOTIFY_EMAIL_TO;
  if (!to) {
    console.error('notify-business-submission: NOTIFY_EMAIL_TO manquante');
    return { statusCode: 500, body: 'NOTIFY_EMAIL_TO not configured' };
  }
  const from = process.env.NOTIFY_EMAIL_FROM || 'Economya <onboarding@resend.dev>';

  const rows = [
    ['Commerce', s.nom_commerce],
    ['Email', s.email],
    ['Catégorie', s.categorie],
    ['Ville', s.ville],
    ['Titre de l\'offre', s.titre_offre],
    ['Dates de validité', s.dates_validite],
    ['Site web', s.site_web],
  ];

  const htmlRows = rows
    .filter(([, v]) => v)
    .map(([k, v]) => `<tr><td style="padding:4px 10px 4px 0;color:#6b7280;font-weight:600;white-space:nowrap">${escapeHtml(k)}</td><td style="padding:4px 0">${escapeHtml(v)}</td></tr>`)
    .join('');

  const html = `
    <div style="font-family:system-ui,-apple-system,sans-serif;max-width:560px">
      <h2 style="margin:0 0 12px">🤝 Nouvelle candidature commerce — Economya Business</h2>
      <table style="border-collapse:collapse;font-size:14px">${htmlRows}</table>
      <p style="margin:16px 0 4px;font-size:14px"><strong>Description :</strong></p>
      <p style="margin:0;font-size:14px;white-space:pre-wrap;color:#111">${escapeHtml(s.description)}</p>
      <p style="margin:20px 0 0"><a href="https://economya.fr/admin-business.html" style="color:#085041;font-weight:700">Voir et traiter la candidature →</a></p>
    </div>
  `;

  // Email interne : prévient l'admin qu'une nouvelle candidature est
  // arrivée (comportement d'origine, inchangé).
  let adminOk = true;
  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from,
        to: [to],
        subject: `Nouvelle candidature commerce : ${s.nom_commerce}`,
        html,
      }),
    });
    if (!res.ok) {
      const errText = await res.text();
      console.error('notify-business-submission: echec Resend (admin)', res.status, errText);
      adminOk = false;
    }
  } catch (e) {
    console.error('notify-business-submission: erreur envoi (admin)', e);
    adminOk = false;
  }

  // Accusé de réception envoyé à l'entreprise elle-même : avant, elle ne
  // recevait strictement rien dans sa boîte mail après avoir déposé son
  // offre, seulement un message à l'écran. Une erreur ici ne doit jamais
  // faire échouer la notification admin ci-dessus, qui est prioritaire.
  let submitterOk = true;
  if (s.email) {
    const submitterHtml = `
      <div style="font-family:system-ui,-apple-system,sans-serif;max-width:560px">
        <h2 style="margin:0 0 12px">✅ Candidature bien reçue</h2>
        <p style="font-size:14px;color:#111">Bonjour,</p>
        <p style="font-size:14px;color:#111">Nous avons bien reçu votre offre <strong>${escapeHtml(s.titre_offre || '')}</strong> pour <strong>${escapeHtml(s.nom_commerce)}</strong> sur Economya Business.</p>
        <p style="font-size:14px;color:#111">Elle est en cours de vérification. Nous revenons vers vous dès qu'elle est traitée — généralement sous quelques jours.</p>
        <p style="font-size:14px;color:#111;margin-top:20px">À bientôt,<br>L'équipe Economya</p>
      </div>
    `;
    try {
      const res2 = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + apiKey,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from,
          to: [s.email],
          subject: 'Candidature bien reçue — Economya Business',
          html: submitterHtml,
        }),
      });
      if (!res2.ok) {
        const errText2 = await res2.text();
        console.error('notify-business-submission: echec Resend (accusé entreprise)', res2.status, errText2);
        submitterOk = false;
      }
    } catch (e) {
      console.error('notify-business-submission: erreur envoi (accusé entreprise)', e);
      submitterOk = false;
    }
  }

  if (!adminOk && !submitterOk) {
    return { statusCode: 502, body: 'Both notifications failed' };
  }
  return { statusCode: 200, body: JSON.stringify({ adminOk, submitterOk }) };
};
