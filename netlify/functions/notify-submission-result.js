// netlify/functions/notify-submission-result.js
//
// Appelee directement depuis admin-business.html (pas via un Database
// Webhook Supabase) juste apres que l'admin a publie ou rejete une
// candidature commerce, pour prevenir l'entreprise du resultat. Avant
// cette fonction, l'entreprise ne pouvait savoir ce qu'il etait advenu
// de son offre qu'en repensant a revenir consulter son tableau de bord
// (compte-entreprise.html) — desormais un email part automatiquement.
//
// Reutilise les memes variables d'environnement Netlify que les autres
// fonctions email du site :
//   - RESEND_API_KEY   : cle API Resend
//   - NOTIFY_EMAIL_FROM : adresse d'expedition (domaine verifie)
//
// Body attendu (JSON) :
//   { email, nom_commerce, titre_offre, result: 'published' | 'rejected', partenariat? }
//
// En cas d'erreur, repond par un statut d'erreur mais ne doit jamais
// bloquer le flux de publication/rejet cote admin-business.html, qui a
// deja eu lieu avant cet appel.

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

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error('notify-submission-result: RESEND_API_KEY manquante');
    return { statusCode: 500, body: 'RESEND_API_KEY not configured' };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || '{}');
  } catch (e) {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const { email, nom_commerce, titre_offre, result, partenariat } = payload;
  if (!email || !result) {
    return { statusCode: 400, body: 'Missing email or result' };
  }
  if (result !== 'published' && result !== 'rejected') {
    return { statusCode: 400, body: 'Invalid result' };
  }

  const from = process.env.NOTIFY_EMAIL_FROM || 'Economya <onboarding@resend.dev>';

  let subject, html;
  if (result === 'published') {
    subject = 'Votre offre est en ligne — Economya Business';
    html = `
      <div style="font-family:system-ui,-apple-system,sans-serif;max-width:560px">
        <h2 style="margin:0 0 12px">✅ Votre offre est publiée</h2>
        <p style="font-size:14px;color:#111">Bonjour,</p>
        <p style="font-size:14px;color:#111">Bonne nouvelle : votre offre <strong>${escapeHtml(titre_offre || '')}</strong> pour <strong>${escapeHtml(nom_commerce || '')}</strong> est maintenant publiée sur Economya Business${partenariat ? ', avec une mise en avant active pendant 7 jours' : ''}.</p>
        <p style="font-size:14px;color:#111">Vous pouvez suivre son statut à tout moment depuis votre espace entreprise.</p>
        <p style="margin:20px 0 0"><a href="https://economya.fr/compte-entreprise.html" style="color:#085041;font-weight:700">Voir mon espace entreprise →</a></p>
      </div>
    `;
  } else {
    subject = 'Votre offre n\'a pas été retenue — Economya Business';
    html = `
      <div style="font-family:system-ui,-apple-system,sans-serif;max-width:560px">
        <h2 style="margin:0 0 12px">Votre offre n'a pas été retenue</h2>
        <p style="font-size:14px;color:#111">Bonjour,</p>
        <p style="font-size:14px;color:#111">Après vérification, votre offre <strong>${escapeHtml(titre_offre || '')}</strong> pour <strong>${escapeHtml(nom_commerce || '')}</strong> n'a pas pu être publiée sur Economya Business.</p>
        <p style="font-size:14px;color:#111">N'hésitez pas à nous recontacter si vous souhaitez plus de précisions, ou à déposer une nouvelle offre.</p>
      </div>
    `;
  }

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ from, to: [email], subject, html }),
    });
    if (!res.ok) {
      const errText = await res.text();
      console.error('notify-submission-result: echec Resend', res.status, errText);
      return { statusCode: 502, body: 'Resend error: ' + errText };
    }
  } catch (e) {
    console.error('notify-submission-result: erreur envoi', e);
    return { statusCode: 500, body: 'Send failed' };
  }

  return { statusCode: 200, body: 'OK' };
};
