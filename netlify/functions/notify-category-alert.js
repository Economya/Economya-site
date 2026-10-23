// netlify/functions/notify-category-alert.js
//
// Recoit le webhook Supabase declenche a chaque nouvelle ligne inseree
// dans la table astuces, et — uniquement quand il s'agit d'une offre
// business publiee "en partenariat" (mise en avant payante, voir
// admin-business.html / publish()) — previent par email tous les
// utilisateurs abonnes a la categorie concernee (table alerts).
//
// Les offres gratuites et les astuces de particuliers n'envoient
// aucune alerte : c'est le avantage concret promis par le palier
// "Mise en avant" de /economya-business.
//
// Configuration necessaire (variables d'environnement Netlify) :
//   - SUPABASE_SERVICE_ROLE_KEY : cle service_role du projet Supabase
//                                 (Project Settings > API > service_role).
//                                 NE JAMAIS exposer cette cle cote client :
//                                 elle contourne les RLS et permet de lire
//                                 les emails des utilisateurs. Elle ne vit
//                                 que dans cette fonction serveur.
//   - RESEND_API_KEY           : deja utilisee par notify-business-submission.
//   - NOTIFY_EMAIL_FROM        : optionnel, adresse d'expedition
//                                 (defaut : alertes@economya.fr, qui
//                                 fonctionne car le domaine economya.fr
//                                 est verifie dans Resend).
//   - WEBHOOK_SECRET           : optionnel, meme mecanisme que pour
//                                 notify-business-submission (header
//                                 x-webhook-secret), si defini il
//                                 s'applique aux deux fonctions.
//
// A configurer cote Supabase : un second Database Webhook, table
// "astuces", evenement Insert uniquement, URL
// https://economya.fr/.netlify/functions/notify-category-alert
//
// En cas d'erreur, la fonction ne doit jamais faire echouer
// l'insertion Supabase elle-meme (deja faite avant l'appel du webhook).

const SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
const MAX_SUBSCRIBERS = 300; // garde-fou anti-emballement

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function slugify(s) {
  return String(s || '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
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

  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!serviceKey) {
    console.error('notify-category-alert: SUPABASE_SERVICE_ROLE_KEY manquante');
    return { statusCode: 500, body: 'SUPABASE_SERVICE_ROLE_KEY not configured' };
  }
  const resendKey = process.env.RESEND_API_KEY;
  if (!resendKey) {
    console.error('notify-category-alert: RESEND_API_KEY manquante');
    return { statusCode: 500, body: 'RESEND_API_KEY not configured' };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || '{}');
  } catch (e) {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const record = payload.record || payload;
  if (!record || !record.id) {
    return { statusCode: 400, body: 'Missing record' };
  }

  // Seules les offres business publiees "en partenariat" declenchent une alerte.
  if (!record.partenariat || !record.enseigne) {
    return { statusCode: 200, body: 'Skipped (not a featured business offer)' };
  }
  if (!record.categorie) {
    return { statusCode: 200, body: 'Skipped (no categorie)' };
  }

  const svHeaders = {
    apikey: serviceKey,
    Authorization: 'Bearer ' + serviceKey,
    'Content-Type': 'application/json',
  };

  // 1. Abonnes a cette categorie.
  let subscribers;
  try {
    const res = await fetch(
      SUPABASE_URL + '/rest/v1/alerts?select=user_id&categorie=eq.' + encodeURIComponent(record.categorie) + '&limit=' + MAX_SUBSCRIBERS,
      { headers: svHeaders }
    );
    if (!res.ok) throw new Error(await res.text());
    subscribers = await res.json();
  } catch (e) {
    console.error('notify-category-alert: echec lecture alerts', e);
    return { statusCode: 502, body: 'Failed to read alerts' };
  }

  const userIds = [...new Set((subscribers || []).map((s) => s.user_id).filter(Boolean))];
  if (userIds.length === 0) {
    return { statusCode: 200, body: 'No subscribers for this category' };
  }

  // 2. Email de chaque abonne (table auth.users, accessible uniquement via
  //    l'API admin + service_role — jamais exposee cote client).
  const emails = [];
  for (const uid of userIds) {
    try {
      const res = await fetch(SUPABASE_URL + '/auth/v1/admin/users/' + uid, { headers: svHeaders });
      if (!res.ok) continue;
      const u = await res.json();
      if (u && u.email) emails.push(u.email);
    } catch (e) {
      console.error('notify-category-alert: echec lecture email', uid, e);
    }
  }
  const uniqueEmails = [...new Set(emails)];
  if (uniqueEmails.length === 0) {
    return { statusCode: 200, body: 'No resolvable emails for subscribers' };
  }

  // 3. Envoi des emails (un par destinataire, pour ne jamais exposer
  //    une adresse a un autre abonne).
  const from = process.env.NOTIFY_EMAIL_FROM || 'Economya <alertes@economya.fr>';
  const link = 'https://economya.fr/astuces/post/' + record.id + '-' + slugify(record.titre) + '?from=business';
  const subject = 'Nouvelle offre dans votre catégorie : ' + (record.categorie || '');
  const html = `
    <div style="font-family:system-ui,-apple-system,sans-serif;max-width:560px">
      <h2 style="margin:0 0 12px">💼 Nouvelle offre partenaire — ${escapeHtml(record.categorie)}</h2>
      <p style="font-size:15px;margin:0 0 6px"><strong>${escapeHtml(record.enseigne)}</strong></p>
      <p style="font-size:15px;margin:0 0 16px">${escapeHtml(record.titre)}</p>
      <p style="margin:0"><a href="${escapeHtml(link)}" style="color:#085041;font-weight:700">Voir l'offre sur Economya →</a></p>
      <p style="margin-top:28px;font-size:12px;color:#9ca3af">Vous recevez cet email car vous êtes abonné(e) aux alertes de cette catégorie sur Economya. Vous pouvez vous désabonner depuis la page Community.</p>
    </div>
  `;

  let sent = 0;
  let failed = 0;
  for (const to of uniqueEmails) {
    try {
      const res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + resendKey,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ from, to: [to], subject, html }),
      });
      if (res.ok) sent++;
      else { failed++; console.error('notify-category-alert: echec Resend pour', to, res.status, await res.text()); }
    } catch (e) {
      failed++;
      console.error('notify-category-alert: erreur envoi', to, e);
    }
  }

  return { statusCode: 200, body: JSON.stringify({ sent, failed, totalSubscribers: userIds.length }) };
};
