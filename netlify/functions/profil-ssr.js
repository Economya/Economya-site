// netlify/functions/profil-ssr.js
//
// Rend côté serveur le <title>, la meta description, le canonical, les
// balises Open Graph / Twitter / JSON-LD, et un aperçu du profil, AVANT
// que le JavaScript client (profil.html) ne prenne le relais.
//
// Même logique que astuce-ssr.js (voir ce fichier pour le contexte
// complet) : avant ce correctif, Netlify servait directement le fichier
// statique profil.html pour toutes les URLs /profil/<pseudo> — son HTML
// brut contient un titre et une description génériques, identiques pour
// TOUS les membres, le vrai contenu n'arrivant qu'après l'appel Supabase
// déclenché par le JS. Résultat : Google voit ~autant de pages qui se
// ressemblent toutes que de membres, ce qui ressemble à du contenu en
// double et nuit à l'indexation ; et un lien de profil partagé sur
// WhatsApp/Facebook n'affiche aucun aperçu personnalisé.
//
// Cette fonction va chercher le gabarit profil.html en production,
// interroge Supabase pour récupérer le profil + un résumé de son
// activité (nombre d'astuces, votes reçus), puis injecte titre,
// description, balises SEO/partage et un aperçu dans le HTML avant de
// le renvoyer. Le JS client prend ensuite le relais normalement pour
// l'interactivité (follow, journal, édition du profil si c'est le
// sien, etc.) — rien n'est retiré côté utilisateur.
//
// Ne reproduit volontairement PAS toute la logique de profil.html
// (abonnés, journal, rang, etc.) : seulement ce qui sert au SEO et à
// l'aperçu de partage. Le reste reste géré par le JS client, comme
// avant.
//
// En cas d'erreur (profil introuvable, Supabase indisponible, etc.),
// la fonction renvoie simplement le profil.html original tel quel :
// aucune régression possible par rapport au comportement actuel.

const SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
const SUPABASE_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';

const TEMPLATE_URL = 'https://economya.fr/profil.html';

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

async function fetchTemplate() {
  const res = await fetch(TEMPLATE_URL);
  if (!res.ok) throw new Error('template fetch failed: ' + res.status);
  return res.text();
}

exports.handler = async function (event) {
  let template;
  try {
    template = await fetchTemplate();
  } catch (e) {
    return { statusCode: 502, body: 'Profil temporairement indisponible.' };
  }

  try {
    // Même astuce que astuce-ssr.js : on lit le pseudo depuis le dernier
    // segment du chemin plutôt que depuis une query string, Netlify ne
    // substituant pas correctement ":splat" dans une query string en
    // production. netlify.toml redirige donc vers
    // /.netlify/functions/profil-ssr/:splat, et ce segment se retrouve
    // en dernière position de event.path.
    const segments = (event.path || '').split('/').filter(Boolean);
    const rawPseudo = segments.length ? segments[segments.length - 1] : '';
    const pseudo = decodeURIComponent(rawPseudo || '');

    if (!pseudo) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
        body: template,
      };
    }

    const profileRes = await fetch(
      SUPABASE_URL +
        '/rest/v1/profiles?pseudo=eq.' +
        encodeURIComponent(pseudo) +
        '&select=id,pseudo,created_at,avatar_url,bio',
      {
        headers: {
          apikey: SUPABASE_KEY,
          Authorization: 'Bearer ' + SUPABASE_KEY,
        },
      }
    );
    const profileRows = profileRes.ok ? await profileRes.json() : [];
    const profile = profileRows && profileRows[0];

    if (!profile) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
        body: template,
      };
    }

    let postsCount = 0;
    let totalVotes = 0;
    try {
      const postsRes = await fetch(
        SUPABASE_URL +
          '/rest/v1/astuces?user_id=eq.' +
          profile.id +
          '&hidden=eq.false&select=votes',
        {
          headers: {
            apikey: SUPABASE_KEY,
            Authorization: 'Bearer ' + SUPABASE_KEY,
          },
        }
      );
      const posts = postsRes.ok ? await postsRes.json() : [];
      postsCount = posts.length;
      totalVotes = posts.reduce((s, p) => s + (p.votes || 0), 0);
    } catch (e) {
      // pas bloquant : on affiche le profil sans les stats si ça échoue
    }

    const canonicalUrl =
      'https://economya.fr/profil/' + encodeURIComponent(profile.pseudo);

    const statsLine =
      postsCount > 0
        ? postsCount +
          ' astuce' +
          (postsCount > 1 ? 's' : '') +
          ' partagée' +
          (postsCount > 1 ? 's' : '') +
          ' · ' +
          totalVotes +
          ' vote' +
          (totalVotes > 1 ? 's' : '') +
          ' reçu' +
          (totalVotes > 1 ? 's' : '')
        : 'Membre de la communauté Economya';

    const rawDesc =
      profile.bio && profile.bio.trim()
        ? profile.bio.trim()
        : 'Profil de ' + profile.pseudo + ' sur Economya. ' + statsLine + '.';
    const desc = rawDesc.slice(0, 155) + (rawDesc.length > 155 ? '…' : '');
    const titleText = profile.pseudo + ' — Economya Community';

    let html = template;

    html = html.replace(
      '<title>Profil — Economya Community</title>',
      '<title>' + escapeHtml(titleText) + '</title>'
    );
    html = html.replace(
      '<meta name="description" content="Consultez le profil d\'un membre de la communauté Economya : ses astuces publiées, ses votes et son activité.">',
      '<meta name="description" content="' + escapeHtml(desc) + '">'
    );
    html = html.replace(
      '<link rel="canonical" href="https://economya.fr/profil" />',
      '<link rel="canonical" href="' + canonicalUrl + '" />'
    );

    const jsonLd = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'ProfilePage',
      name: titleText,
      url: canonicalUrl,
      mainEntity: {
        '@type': 'Person',
        name: profile.pseudo,
        url: canonicalUrl,
      },
    });

    const extraHead =
      '<meta property="og:type" content="profile">\n' +
      '<meta property="og:site_name" content="Economya.fr">\n' +
      '<meta property="og:title" content="' + escapeHtml(titleText) + '">\n' +
      '<meta property="og:description" content="' + escapeHtml(desc) + '">\n' +
      '<meta property="og:url" content="' + canonicalUrl + '">\n' +
      '<meta property="og:image" content="https://economya.fr/og-image.png">\n' +
      '<meta name="twitter:card" content="summary">\n' +
      '<meta name="twitter:title" content="' + escapeHtml(titleText) + '">\n' +
      '<meta name="twitter:description" content="' + escapeHtml(desc) + '">\n' +
      '<script type="application/ld+json">' + jsonLd + '</script>\n' +
      '</head>';

    html = html.replace('</head>', extraHead);

    const snapshot =
      '<div class="loading" style="text-align:center">' +
      '<h1 style="font-size:1.3rem;margin-bottom:.4rem">' +
      escapeHtml(profile.pseudo) +
      '</h1>' +
      '<p>' +
      escapeHtml(statsLine) +
      '</p>' +
      '</div>';

    html = html.replace(
      '<div id="content"><div class="loading">Chargement du profil...</div></div>',
      '<div id="content">' + snapshot + '</div>'
    );

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control':
          'public, max-age=0, s-maxage=300, stale-while-revalidate=600',
      },
      body: html,
    };
  } catch (e) {
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'text/html; charset=utf-8' },
      body: template,
    };
  }
};
