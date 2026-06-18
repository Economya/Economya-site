import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
fichiers_modifies = 0
fichiers_erreur = 0

for fichier in os.listdir(dossier):
    if not fichier.endswith('.html'):
        continue

    chemin = os.path.join(dossier, fichier)

    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            contenu = f.read()

        # Vérifier si Open Graph déjà présent
        if 'og:title' in contenu:
            continue

        # Extraire le titre
        titre_match = re.search(r'<title>(.*?)</title>', contenu)
        titre = titre_match.group(1) if titre_match else 'Economya.fr'
        titre = titre.replace(' — Economya.fr', '').replace(' - Economya.fr', '').strip()

        # Extraire la description
        desc_match = re.search(r'<meta name="description" content="(.*?)"', contenu)
        description = desc_match.group(1) if desc_match else 'Conseils, outils et astuces pour économiser au quotidien sur Economya.fr'

        # URL de la page
        url = f'https://economya.fr/{fichier}'

        # Balises Open Graph
        og_tags = f'''
  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Economya.fr">
  <meta property="og:title" content="{titre}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://economya.fr/og-image.svg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="fr_FR">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{titre}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="https://economya.fr/og-image.svg">'''

        # Insérer avant </head>
        if '</head>' in contenu:
            contenu = contenu.replace('</head>', og_tags + '\n</head>', 1)
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(contenu)
            fichiers_modifies += 1

    except Exception as e:
        fichiers_erreur += 1
        print(f"Erreur sur {fichier}: {e}")

print(f"✅ {fichiers_modifies} fichiers modifiés")
print(f"❌ {fichiers_erreur} erreurs")
