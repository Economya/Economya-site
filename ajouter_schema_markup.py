import os
import re
import json

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

        # Vérifier si schema déjà présent
        if 'application/ld+json' in contenu:
            continue

        # Extraire le titre
        titre_match = re.search(r'<title>(.*?)</title>', contenu)
        titre = titre_match.group(1) if titre_match else 'Economya.fr'
        titre = titre.replace(' — Economya.fr', '').replace(' - Economya.fr', '').strip()

        # Extraire la description
        desc_match = re.search(r'<meta name="description" content="(.*?)"', contenu)
        description = desc_match.group(1) if desc_match else 'Conseils et astuces pour économiser au quotidien.'

        # URL de la page
        url = f'https://economya.fr/{fichier}'

        # Détecter le type de page
        if 'quiz' in fichier or 'test-' in fichier:
            schema_type = 'Quiz'
        elif 'calculateur' in fichier or 'simulateur' in fichier or 'comparateur' in fichier or 'generateur' in fichier:
            schema_type = 'WebApplication'
        else:
            schema_type = 'Article'

        if schema_type == 'Article':
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": titre,
                "description": description,
                "url": url,
                "publisher": {
                    "@type": "Organization",
                    "name": "Economya.fr",
                    "url": "https://economya.fr",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://economya.fr/favicon.svg"
                    }
                },
                "inLanguage": "fr-FR"
            }
        elif schema_type == 'WebApplication':
            schema = {
                "@context": "https://schema.org",
                "@type": "WebApplication",
                "name": titre,
                "description": description,
                "url": url,
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "Web",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "EUR"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Economya.fr",
                    "url": "https://economya.fr"
                },
                "inLanguage": "fr-FR"
            }
        else:
            schema = {
                "@context": "https://schema.org",
                "@type": "Quiz",
                "name": titre,
                "description": description,
                "url": url,
                "publisher": {
                    "@type": "Organization",
                    "name": "Economya.fr",
                    "url": "https://economya.fr"
                },
                "inLanguage": "fr-FR"
            }

        schema_tag = f'\n  <script type="application/ld+json">\n  {json.dumps(schema, ensure_ascii=False, indent=2)}\n  </script>'

        # Insérer avant </head>
        if '</head>' in contenu:
            contenu = contenu.replace('</head>', schema_tag + '\n</head>', 1)
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(contenu)
            fichiers_modifies += 1

    except Exception as e:
        fichiers_erreur += 1
        print(f"Erreur sur {fichier}: {e}")

print(f"✅ {fichiers_modifies} fichiers modifiés")
print(f"❌ {fichiers_erreur} erreurs")
