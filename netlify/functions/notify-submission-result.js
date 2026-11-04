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
// Securite : la fonction n'accepte AUCUNE adresse ni aucun texte dans la
// requete. Elle exige le jeton de session d'un administrateur
// (profiles.is_admin), relit elle-meme la candidature dans Supabase et
// n'ecrit qu'a l'adresse enregistree sur cette candidature. Elle ne peut
// donc pas servir a envoyer des e-mails arbitraires depuis le domaine.
//
// Body attendu (JSON) :
//   { submission_id, result: 'published' | 'rejected', partenariat? }
// Header : Authorization: Bearer <jeton de session de l'admin>
//
// En cas d'erreur, repond par un statut d'erreur mais ne doit jamais
// bloquer le flux de publication/rejet cote admin-business.html, qui a
// deja eu lieu avant cet appel.

const SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
// Cle publique (anon) du projet, deja presente dans le code du site.
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';

async function sb(path, token) {
  const res = await fetch(SUPABASE_URL + path, {
    headers: { apikey: SUPABASE_KEY, Authorization: 'Bearer ' + token },
  });
  if (!res.ok) return null;
  return res.json();
}

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

  const { submission_id, result, partenariat } = payload;
  if (!submission_id || !result) {
    return { statusCode: 400, body: 'Missing submission_id or result' };
  }
  if (result !== 'published' && result !== 'rejected') {
    return { statusCode: 400, body: 'Invalid result' };
  }

  // 1. Jeton de session obligatoire.
  const auth = event.headers.authorization || event.headers.Authorization || '';
  const token = auth.replace(/^Bearer\s+/i, '');
  if (!token) {
    return { statusCode: 401, body: 'Missing token' };
  }

  let email, nom_commerce, titre_offre;
  try {
    // 2. Le jeton doit etre valide ...
    const user = await sb('/auth/v1/user', token);
    if (!user || !user.id) {
      return { statusCode: 401, body: 'Invalid token' };
    }
    // 3. ... et appartenir a un administrateur.
    const prof = await sb('/rest/v1/profiles?id=eq.' + encodeURIComponent(user.id) + '&select=is_admin', token);
    if (!prof || !prof[0] || !prof[0].is_admin) {
      return { statusCode: 403, body: 'Forbidden' };
    }
    // 4. L'adresse et les textes viennent de la base, pas de la requete.
    const rows = await sb('/rest/v1/business_submissions?id=eq.' + encodeURIComponent(String(submission_id)) + '&select=email,nom_commerce,titre_offre,status', token);
    const sub = rows && rows[0];
    if (!sub || !sub.email) {
      return { statusCode: 404, body: 'Submission not found' };
    }
    // 5. Le resultat demande doit correspondre au statut reel enregistre.
    if (sub.status !== result) {
      return { statusCode: 409, body: 'Status mismatch' };
    }
    email = sub.email;
    nom_commerce = sub.nom_commerce;
    titre_offre = sub.titre_offre;
  } catch (e) {
    console.error('notify-submission-result: erreur verification', e);
    return { statusCode: 500, body: 'Verification failed' };
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
      return { statusCode: 502, body: 'Resend error' };
    }
  } catch (e) {
    console.error('notify-submission-result: erreur envoi', e);
    return { statusCode: 500, body: 'Send failed' };
  }

  return { statusCode: 200, body: 'OK' };
};
