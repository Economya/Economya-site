// netlify/functions/notify-account-deleted.js
//
// Appelee depuis profil.html juste avant la suppression du compte, pour
// envoyer au titulaire un e-mail qui confirme que sa demande de suppression
// a ete prise en compte (bonne pratique : il est prevenu meme si quelqu'un
// d'autre avait acces a sa session).
//
// Securite : la fonction n'accepte AUCUNE adresse dans la requete. Elle
// verifie le jeton de session aupres de Supabase et n'ecrit qu'a l'adresse
// e-mail du compte authentifie. Elle ne peut donc pas servir a envoyer des
// e-mails a des tiers.
//
// Variables d'environnement Netlify deja utilisees par les autres fonctions :
//   - RESEND_API_KEY    : cle API Resend
//   - NOTIFY_EMAIL_FROM : adresse d'expedition (domaine verifie)

const SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
// Cle publique (anon) du projet, deja presente dans le code du site.
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error('notify-account-deleted: RESEND_API_KEY manquante');
    return { statusCode: 500, body: 'RESEND_API_KEY not configured' };
  }

  const auth = event.headers.authorization || event.headers.Authorization || '';
  const token = auth.replace(/^Bearer\s+/i, '');
  if (!token) {
    return { statusCode: 401, body: 'Missing token' };
  }

  // Verifie le jeton et recupere l'adresse e-mail du compte.
  let email;
  try {
    const res = await fetch(SUPABASE_URL + '/auth/v1/user', {
      headers: { apikey: SUPABASE_KEY, Authorization: 'Bearer ' + token },
    });
    if (!res.ok) {
      return { statusCode: 401, body: 'Invalid token' };
    }
    const user = await res.json();
    email = user && user.email;
  } catch (e) {
    console.error('notify-account-deleted: erreur verification', e);
    return { statusCode: 500, body: 'Verification failed' };
  }
  if (!email) {
    return { statusCode: 400, body: 'No email on account' };
  }

  const from = process.env.NOTIFY_EMAIL_FROM || 'Economya <onboarding@resend.dev>';
  const date = new Date().toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Paris',
  });
  const subject = 'Votre compte Economya est supprimé';
  const html = `
    <div style="font-family:system-ui,-apple-system,sans-serif;max-width:560px">
      <h2 style="margin:0 0 12px">Votre demande de suppression a bien été prise en compte</h2>
      <p style="font-size:14px;color:#111">Bonjour,</p>
      <p style="font-size:14px;color:#111">Le ${date}, une demande de suppression de votre compte Economya a été effectuée depuis votre session. Votre compte, votre photo de profil, vos astuces, vos votes et vos images de preuve sont supprimés.</p>
      <p style="font-size:14px;color:#111">Vous n'avez rien d'autre à faire. Si vous n'êtes pas à l'origine de cette demande, écrivez-nous sans attendre à <a href="mailto:contact@economya.fr" style="color:#085041;font-weight:700">contact@economya.fr</a>.</p>
      <p style="font-size:12px;color:#666;margin-top:20px">Pour en savoir plus sur vos données, consultez notre <a href="https://economya.fr/politique-confidentialite" style="color:#085041">politique de confidentialité</a>.</p>
    </div>
  `;

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ from, to: [email], subject, html }),
    });
    if (!res.ok) {
      const errText = await res.text();
      console.error('notify-account-deleted: echec Resend', res.status, errText);
      return { statusCode: 502, body: 'Resend error' };
    }
  } catch (e) {
    console.error('notify-account-deleted: erreur envoi', e);
    return { statusCode: 500, body: 'Send failed' };
  }

  return { statusCode: 200, body: 'OK' };
};
