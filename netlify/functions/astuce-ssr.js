// netlify/functions/astuce-ssr.js
//
// Rend côté serveur le <title>, la meta description, les balises
// Open Graph / Twitter / JSON-LD, et un aperçu texte de l'astuce,
// AVANT que le JavaScript client (astuce.html) ne prenne le relais.
//
// Avant ce correctif, Netlify servait directement le fichier statique
// astuce.html : son HTML brut contenait un titre générique
// ("Astuce — Economya.fr") et un message "Chargement de l'astuce…",
// le vrai contenu n'arrivant qu'après un appel Supabase déclenché par
// le JS. Les robots / aperçus de partage qui ne lisent que le HTML
// brut ne voyaient donc jamais le vrai titre ni le vrai texte.
//
// Cette fonction va chercher le modèle actuel de astuce.html en
// production (toujours la version déployée la plus récente — pas de
// copie à maintenir en double), interroge Supabase pour récupérer
// l'astuce correspondante, puis injecte le titre, la description,
// les balises SEO/partage et un aperçu du texte dans le HTML avant de
// le renvoyer. Le JS client s'exécute ensuite normalement par-dessus
// pour l'interactivité (votes, commentaires, etc.) — rien n'est
// retiré côté utilisateur.
//
// En cas d'erreur (astuce introuvable, Supabase indisponible, etc.),
// la fonction renvoie simplement le astuce.html original tel quel :
// aucune régression possible par rapport au comportement actuel.

const SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
const SUPABASE_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';

const TEMPLATE_URL = 'https://economya.fr/astuce.html';

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function slugify(str) {
  return String(str || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60);
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
    return { statusCode: 502, body: 'Astuce temporairement indisponible.' };
  }

  try {
    const rawSlug =
      (event.queryStringParameters && event.queryStringParameters.slug) || '';
    const decoded = decodeURIComponent(rawSlug);
    const idMatch = decoded.match(/^(\d+)/);
    const id = idMatch ? idMatch[1] : null;

    if (!id) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
        body: template,
      };
    }

    const apiRes = await fetch(
      SUPABASE_URL + '/rest/v1/astuces?id=eq.' + id + '&select=*',
      {
        headers: {
          apikey: SUPABASE_KEY,
          Authorization: 'Bearer ' + SUPABASE_KEY,
        },
      }
    );
    const rows = apiRes.ok ? await apiRes.json() : [];
    const p = rows && rows[0];

    if (!p || p.hidden) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
        body: template,
      };
    }

    const slug = slugify(p.titre);
    const canonicalUrl =
      'https://economya.fr/astuces/post/' + p.id + (slug ? '-' + slug : '');
    const rawDesc = p.description || '';
    const desc =
      rawDesc.slice(0, 155) + (rawDesc.length > 155 ? '…' : '');
    const titleText = p.titre + ' — Economya.fr';

    let html = template;

    html = html.replace(
      '<title id="pageTitle">Astuce — Economya.fr</title>',
      '<title id="pageTitle">' + escapeHtml(titleText) + '</title>'
    );
    html = html.replace(
      '<meta id="metaDesc" name="description" content="Découvrez une astuce pour économiser partagée par la communauté Economya.fr.">',
      '<meta id="metaDesc" name="description" content="' +
        escapeHtml(desc) +
        '">'
    );

    const jsonLd = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'DiscussionForumPosting',
      headline: p.titre,
      text: p.description,
      datePublished: p.created_at,
      url: canonicalUrl,
      author: { '@type': 'Person', name: p.auteur || 'Membre Economya' },
      interactionStatistic: [
        {
          '@type': 'InteractionCounter',
          interactionType: 'https://schema.org/LikeAction',
          userInteractionCount: p.votes || 0,
        },
      ],
      publisher: {
        '@type': 'Organization',
        name: 'Economya.fr',
        url: 'https://economya.fr',
      },
    });

    const extraHead =
      '<link rel="canonical" href="' + canonicalUrl + '">\n' +
      '<meta property="og:type" content="article">\n' +
      '<meta property="og:site_name" content="Economya.fr">\n' +
      '<meta property="og:title" content="' + escapeHtml(p.titre) + '">\n' +
      '<meta property="og:description" content="' + escapeHtml(desc) + '">\n' +
      '<meta property="og:url" content="' + canonicalUrl + '">\n' +
      '<meta property="og:image" content="https://economya.fr/og-image.svg">\n' +
      '<meta name="twitter:card" content="summary_large_image">\n' +
      '<meta name="twitter:title" content="' + escapeHtml(p.titre) + '">\n' +
      '<meta name="twitter:description" content="' + escapeHtml(desc) + '">\n' +
      '<script type="application/ld+json">' + jsonLd + '</script>\n' +
      '</head>';

    html = html.replace('</head>', extraHead);

    const savingLine =
      p.economie > 0
        ? '<p style="margin-top:10px;font-weight:700;color:#166534">💰 ' +
          Number(p.economie).toLocaleString('fr-FR') +
          '€ économisés</p>'
        : '';

    const snapshot =
      '<div class="card">' +
      '<h1 class="post-title">' + escapeHtml(p.titre) + '</h1>' +
      '<p class="post-cat">' + escapeHtml(p.categorie || '') + '</p>' +
      '<div class="post-body">' + escapeHtml(p.description || '') + '</div>' +
      savingLine +
      '</div>';

    html = html.replace(
      '<div class="state">Chargement de l\'astuce…</div>',
      snapshot
    );

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=0, s-maxage=300, stale-while-revalidate=600',
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
