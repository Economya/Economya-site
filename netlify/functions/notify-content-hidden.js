// netlify/functions/notify-content-hidden.js
//
// Appelee depuis moderation.html juste apres qu'un administrateur a masque
// une astuce ou un commentaire. Elle previent l'auteur par e-mail, avec le
// motif de la decision, comme le promettent la page /signalement (art. 4)
// et les CGU. L'auteur peut contester en ecrivant a contact@economya.fr.
//
// Securite : la fonction n'accepte ni adresse ni texte libre autre que le
// motif. Elle exige le jeton de session d'un administrateur (profiles.is_admin),
// relit le contenu dans Supabase, verifie qu'il est bien masque, puis
// recupere l'adresse de l'auteur cote serveur (cle service_role, jamais
// exposee au navigateur). Elle ne peut donc pas servir a envoyer des
// e-mails arbitraires.
//
// Variables d'environnement Netlify : RESEND_API_KEY, NOTIFY_EMAIL_FROM,
// SUPABASE_SERVICE_ROLE_KEY.
//
// Body (JSON) : { type: 'astuce' | 'comment', id, categorie, detail? }
//   categorie = une cle de MOTIFS ci-dessous ; detail = precisions facultatives.
// Header      : Authorization: Bearer <jeton de session de l'admin>

const SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
// Cle publique (anon) du projet, deja presente dans le code du site.
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';

// Libelles des motifs : definis ici cote serveur, jamais pris dans la requete.
const MOTIFS = {
  illegal: 'Contenu illégal ou incitant à la haine',
  diffamation: 'Propos diffamatoires, injurieux ou discriminatoires',
  droits: "Atteinte aux droits d'un tiers (droit d'auteur, droit à l'image, vie privée)",
  trompeur: 'Astuce ou offre trompeuse ou fausse',
  spam: 'Spam, publicité ou démarchage non autorisés',
  usurpation: "Usurpation d'identité",
  partenariat: 'Offre commerciale non signalée comme partenariat',
  autre: 'Autre motif',
};

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

async function sb(path, token) {
  const res = await fetch(SUPABASE_URL + path, {
    headers: { apikey: SUPABASE_KEY, Authorization: 'Bearer ' + token },
  });
  if (!res.ok) return null;
  return res.json();
}

function reply(statusCode, obj) {
  return { statusCode, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(obj) };
}

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return reply(405, { error: 'Method Not Allowed' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!apiKey || !serviceKey) {
    console.error('notify-content-hidden: variable d\'environnement manquante');
    return reply(500, { error: 'Not configured' });
  }

  let payload;
  try {
    payload = JSON.parse(event.body || '{}');
  } catch (e) {
    return reply(400, { error: 'Invalid JSON' });
  }
  const type = payload.type;
  const id = payload.id;
  const categorie = String(payload.categorie || '');
  const detail = String(payload.detail || '').trim().slice(0, 500);
  if ((type !== 'astuce' && type !== 'comment') || !id || !Object.prototype.hasOwnProperty.call(MOTIFS, categorie)) {
    return reply(400, { error: 'Missing type, id or categorie' });
  }
  if (categorie === 'autre' && detail.length < 3) {
    return reply(400, { error: 'Detail required for categorie autre' });
  }

  const auth = event.headers.authorization || event.headers.Authorization || '';
  const token = auth.replace(/^Bearer\s+/i, '');
  if (!token) {
    return reply(401, { error: 'Missing token' });
  }

  let authorId, label;
  try {
    // 1. Jeton valide et appartenant a un administrateur.
    const user = await sb('/auth/v1/user', token);
    if (!user || !user.id) return reply(401, { error: 'Invalid token' });
    const prof = await sb('/rest/v1/profiles?id=eq.' + encodeURIComponent(user.id) + '&select=is_admin', token);
    if (!prof || !prof[0] || !prof[0].is_admin) return reply(403, { error: 'Forbidden' });

    // 2. Le contenu vient de la base et doit etre masque.
    const table = type === 'astuce' ? 'astuces' : 'astuce_comments';
    const cols = type === 'astuce' ? 'user_id,titre,hidden' : 'user_id,contenu,hidden';
    const rows = await sb('/rest/v1/' + table + '?id=eq.' + encodeURIComponent(String(id)) + '&select=' + cols, token);
    const row = rows && rows[0];
    if (!row) return reply(404, { error: 'Not found' });
    if (row.hidden !== true) return reply(409, { error: 'Content is not hidden' });
    if (!row.user_id) return reply(200, { sent: false, reason: 'no_user' });
    authorId = row.user_id;
    label = type === 'astuce' ? row.titre : String(row.contenu || '').slice(0, 120);
  } catch (e) {
    console.error('notify-content-hidden: erreur verification', e);
    return reply(500, { error: 'Verification failed' });
  }

  // 3. Adresse de l'auteur, lue cote serveur.
  let email;
  try {
    const res = await fetch(SUPABASE_URL + '/auth/v1/admin/users/' + encodeURIComponent(authorId), {
      headers: { apikey: serviceKey, Authorization: 'Bearer ' + serviceKey },
    });
    if (!res.ok) return reply(200, { sent: false, reason: 'no_user' });
    const u = await res.json();
    email = u && u.email;
  } catch (e) {
    console.error('notify-content-hidden: erreur lecture auteur', e);
    return reply(500, { error: 'Author lookup failed' });
  }
  if (!email) return reply(200, { sent: false, reason: 'no_user' });

  const from = process.env.NOTIFY_EMAIL_FROM || 'Economya <onboarding@resend.dev>';
  const noun = type === 'astuce' ? 'astuce' : 'commentaire';
  const subject = type === 'astuce'
    ? 'Votre astuce a été masquée sur Economya'
    : 'Votre commentaire a été masqué sur Economya';
  const html = `
    <div style="font-family:system-ui,-apple-system,sans-serif;max-width:560px">
      <h2 style="margin:0 0 12px">Votre ${noun} a été masqué</h2>
      <p style="font-size:14px;color:#111">Bonjour,</p>
      <p style="font-size:14px;color:#111">Après examen, nous avons masqué votre ${noun} « ${escapeHtml(label)} » sur Economya.</p>
      <p style="font-size:14px;color:#111"><strong>Motif :</strong> ${escapeHtml(MOTIFS[categorie])}</p>
      ${detail ? `<p style="font-size:14px;color:#111"><strong>Précisions :</strong> ${escapeHtml(detail)}</p>` : ''}
      <p style="font-size:14px;color:#111">Si vous pensez qu'il s'agit d'une erreur, vous pouvez contester cette décision en écrivant à <a href="mailto:contact@economya.fr" style="color:#085041;font-weight:700">contact@economya.fr</a> : votre demande sera réexaminée et une réponse vous sera donnée.</p>
      <p style="font-size:12px;color:#666;margin-top:20px">Voir nos <a href="https://economya.fr/cgu" style="color:#085041">conditions d'utilisation</a> et la <a href="https://economya.fr/signalement" style="color:#085041">procédure de signalement</a>.</p>
    </div>
  `;

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + apiKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to: [email], subject, html }),
    });
    if (!res.ok) {
      console.error('notify-content-hidden: echec Resend', res.status, await res.text());
      return reply(502, { sent: false, reason: 'resend' });
    }
  } catch (e) {
    console.error('notify-content-hidden: erreur envoi', e);
    return reply(500, { sent: false, reason: 'send' });
  }

  return reply(200, { sent: true });
};
