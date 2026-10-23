// netlify/functions/sitemap.js
//
// Avant ce correctif, /sitemap.xml était un fichier statique figé à
// 92 URLs, aucune astuce individuelle (/astuces/post/...) n'y
// figurait : Google n'avait donc aucun moyen simple de découvrir ces
// pages. Cette fonction régénère le sitemap à chaque requête en
// gardant les 92 URLs statiques existantes (copiées telles quelles
// ci-dessous, aucune perdue) et en y ajoutant dynamiquement toutes
// les astuces non masquées, lues en direct depuis Supabase.
//
// netlify.toml redirige /sitemap.xml vers cette fonction avec
// force = true (sinon le vieux fichier statique sitemap.xml, qui
// reste sur le disque comme copie de secours, serait servi en
// priorité par Netlify).

const SUPABASE_URL = 'https://awelbxqiltokhsoddako.supabase.co';
const SUPABASE_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3ZWxieHFpbHRva2hzb2RkYWtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzNTM1MjIsImV4cCI6MjEwNDkyOTUyMn0.pao4Gxw9S7bdfTFExd3W1idWEV76VvykeiZSSf3mQxw';

function escapeXml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
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

// Les 92 URLs statiques, copiées à l'identique depuis l'ancien
// sitemap.xml (mêmes changefreq / priority). Si de nouvelles pages
// statiques sont ajoutées au site plus tard, il faut les ajouter ici
// aussi (ce tableau remplace désormais le fichier statique).
const STATIC_URLS = [
  // Pages principales
  ['https://economya.fr/', 'daily', '1.0'],
  ['https://economya.fr/outils-gratuits', 'weekly', '0.9'],
  ['https://economya.fr/comparateurs', 'weekly', '0.9'],
  ['https://economya.fr/neobanques-2026', 'monthly', '0.85'],
  ['https://economya.fr/banque-en-ligne-vs-traditionnelle', 'monthly', '0.85'],
  ['https://economya.fr/forfaits-5g-pas-cher', 'monthly', '0.85'],
  ['https://economya.fr/vpn-gratuit-payant', 'monthly', '0.85'],
  ['https://economya.fr/recherche', 'weekly', '0.8'],
  ['https://economya.fr/economya-business', 'monthly', '0.8'],
  ['https://economya.fr/lexique-finance', 'monthly', '0.8'],
  ['https://economya.fr/community', 'daily', '0.8'],
  ['https://economya.fr/forum-astuces', 'daily', '0.8'],
  ['https://economya.fr/jeux', 'weekly', '0.9'],
  ['https://economya.fr/a-propos', 'monthly', '0.6'],
  ['https://economya.fr/regles-communaute', 'monthly', '0.5'],
  ['https://economya.fr/mentions-legales', 'yearly', '0.3'],
  ['https://economya.fr/politique-confidentialite', 'yearly', '0.3'],
  ['https://economya.fr/cgu', 'yearly', '0.3'],
  // Outils & calculateurs (22)
  ['https://economya.fr/simulateur-epargne', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-budget', 'monthly', '0.9'],
  ['https://economya.fr/generateur-budget', 'monthly', '0.9'],
  ['https://economya.fr/comparateur-livrets', 'monthly', '0.9'],
  ['https://economya.fr/checklist-abonnements', 'monthly', '0.9'],
  ['https://economya.fr/generateur-defi-epargne', 'monthly', '0.9'],
  ['https://economya.fr/simulateur-credit-immo', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-frais-notaire', 'monthly', '0.9'],
  ['https://economya.fr/simulateur-apl', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-salaire', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-impot', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-prime-activite', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-cout-voiture', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-cout-appartement', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-budget-vacances', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-pouvoir-achat', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-capacite-emprunt', 'monthly', '0.9'],
  ['https://economya.fr/calculateur-rendement-locatif', 'monthly', '0.9'],
  ['https://economya.fr/simulateur-loyer-achat', 'monthly', '0.9'],
  ['https://economya.fr/simulateur-retraite', 'monthly', '0.9'],
  ['https://economya.fr/simulateur-economies-energie', 'monthly', '0.9'],
  ['https://economya.fr/calendrier-bons-plans', 'monthly', '0.9'],
  // Quiz & tests (7)
  ['https://economya.fr/quiz-epargnant', 'monthly', '0.8'],
  ['https://economya.fr/quiz-animal-epargnant', 'monthly', '0.8'],
  ['https://economya.fr/quiz-voyageur', 'monthly', '0.8'],
  ['https://economya.fr/quiz-marque', 'monthly', '0.8'],
  ['https://economya.fr/quiz-personnage-serie', 'monthly', '0.8'],
  ['https://economya.fr/test-surconsommation', 'monthly', '0.8'],
  ['https://economya.fr/vrai-ou-faux', 'monthly', '0.8'],
  // Jeux interactifs (46)
  ['https://economya.fr/adn-financier', 'monthly', '0.7'],
  ['https://economya.fr/attrape-economies', 'monthly', '0.7'],
  ['https://economya.fr/aura-financiere', 'monthly', '0.7'],
  ['https://economya.fr/bar-de-plage', 'monthly', '0.7'],
  ['https://economya.fr/boite-economies', 'monthly', '0.7'],
  ['https://economya.fr/boule-de-patrimoine', 'monthly', '0.7'],
  ['https://economya.fr/budget-run', 'monthly', '0.7'],
  ['https://economya.fr/budget-tower', 'monthly', '0.7'],
  ['https://economya.fr/casse-tes-dettes', 'monthly', '0.7'],
  ['https://economya.fr/chef-econome', 'monthly', '0.7'],
  ['https://economya.fr/chef-resto-v2', 'monthly', '0.7'],
  ['https://economya.fr/coach-econome', 'monthly', '0.7'],
  ['https://economya.fr/domaine-viticole', 'monthly', '0.7'],
  ['https://economya.fr/eclateur-de-dettes', 'monthly', '0.7'],
  ['https://economya.fr/finance-runner-3d-v2', 'monthly', '0.7'],
  ['https://economya.fr/finance-wrapped', 'monthly', '0.7'],
  ['https://economya.fr/grand-prix-epargne', 'monthly', '0.7'],
  ['https://economya.fr/happy-budget', 'monthly', '0.7'],
  ['https://economya.fr/hotel-manager', 'monthly', '0.7'],
  ['https://economya.fr/ile-aux-oeufs', 'monthly', '0.7'],
  ['https://economya.fr/inflation-run', 'monthly', '0.7'],
  ['https://economya.fr/investisseur-virtuel', 'monthly', '0.7'],
  ['https://economya.fr/jackpot-finance', 'monthly', '0.7'],
  ['https://economya.fr/la-machine-a-reves', 'monthly', '0.7'],
  ['https://economya.fr/la-roue-des-scenarios', 'monthly', '0.7'],
  ['https://economya.fr/le-bon-deal', 'monthly', '0.7'],
  ['https://economya.fr/le-gestionnaire-de-crise', 'monthly', '0.7'],
  ['https://economya.fr/le-grand-cycle-economique', 'monthly', '0.7'],
  ['https://economya.fr/le-marche-vivant', 'monthly', '0.7'],
  ['https://economya.fr/le-mur-des-bravos', 'monthly', '0.7'],
  ['https://economya.fr/le-negociateur', 'monthly', '0.7'],
  ['https://economya.fr/le-sosie-celebre-de-ton-epargne', 'monthly', '0.7'],
  ['https://economya.fr/le-trophee-du-jour', 'monthly', '0.7'],
  ['https://economya.fr/marathon-budgetaire-v2', 'monthly', '0.7'],
  ['https://economya.fr/memory-finance', 'monthly', '0.7'],
  ['https://economya.fr/ou-vivre-mieux', 'monthly', '0.7'],
  ['https://economya.fr/pile-ou-face-financier', 'monthly', '0.7'],
  ['https://economya.fr/primo-accedant', 'monthly', '0.7'],
  ['https://economya.fr/prix-party', 'monthly', '0.7'],
  ['https://economya.fr/radar-arnaques', 'monthly', '0.7'],
  ['https://economya.fr/roue-economies', 'monthly', '0.7'],
  ['https://economya.fr/sprint-epargne', 'monthly', '0.7'],
  ['https://economya.fr/tas-combien-dans-les-mains', 'monthly', '0.7'],
  ['https://economya.fr/ton-annee-bons-plans', 'monthly', '0.7'],
  ['https://economya.fr/ton-totem-financier', 'monthly', '0.7'],
  ['https://economya.fr/tri-de-budget', 'monthly', '0.7'],
];

exports.handler = async function () {
  let astuceEntries = [];
  try {
    const res = await fetch(
      SUPABASE_URL +
        '/rest/v1/astuces?select=id,titre,created_at,hidden&or=(hidden.eq.false,hidden.is.null)&order=id.asc',
      {
        headers: {
          apikey: SUPABASE_KEY,
          Authorization: 'Bearer ' + SUPABASE_KEY,
        },
      }
    );
    if (res.ok) {
      const rows = await res.json();
      astuceEntries = rows.map(function (p) {
        const slug = slugify(p.titre);
        const loc =
          'https://economya.fr/astuces/post/' +
          p.id +
          (slug ? '-' + slug : '');
        const lastmod = p.created_at ? String(p.created_at).slice(0, 10) : null;
        return { loc: loc, lastmod: lastmod };
      });
    }
  } catch (e) {
    // Si Supabase est indisponible, on renvoie quand même les 92 URLs
    // statiques plutôt qu'une erreur complète.
  }

  const staticXml = STATIC_URLS.map(function (u) {
    return (
      '  <url><loc>' +
      escapeXml(u[0]) +
      '</loc><changefreq>' +
      u[1] +
      '</changefreq><priority>' +
      u[2] +
      '</priority></url>'
    );
  }).join('\n');

  const astuceXml = astuceEntries
    .map(function (u) {
      return (
        '  <url><loc>' +
        escapeXml(u.loc) +
        '</loc>' +
        (u.lastmod ? '<lastmod>' + u.lastmod + '</lastmod>' : '') +
        '<changefreq>monthly</changefreq><priority>0.6</priority></url>'
      );
    })
    .join('\n');

  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n' +
    '  <!-- Pages statiques -->\n' +
    staticXml +
    '\n\n  <!-- Astuces (générées dynamiquement depuis Supabase) -->\n' +
    (astuceXml || '  <!-- aucune astuce trouvée -->') +
    '\n\n</urlset>\n';

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=0, s-maxage=600, stale-while-revalidate=1800',
    },
    body: body,
  };
};
