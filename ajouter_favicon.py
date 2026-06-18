import os

dossier = "/Users/alexandregoffinet/Desktop/mon site"
fichiers_modifies = 0
fichiers_erreur = 0

favicon_tag = '  <link rel="icon" type="image/svg+xml" href="favicon.svg">'

for fichier in os.listdir(dossier):
    if not fichier.endswith('.html'):
        continue

    chemin = os.path.join(dossier, fichier)

    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            contenu = f.read()

        # Vérifier si favicon déjà présent
        if 'favicon' in contenu:
            continue

        # Insérer après <meta charset
        if '<meta charset' in contenu:
            contenu = contenu.replace('<meta charset', favicon_tag + '\n  <meta charset', 1)
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(contenu)
            fichiers_modifies += 1

    except Exception as e:
        fichiers_erreur += 1
        print(f"Erreur sur {fichier}: {e}")

print(f"✅ {fichiers_modifies} fichiers modifiés")
print(f"❌ {fichiers_erreur} erreurs")
