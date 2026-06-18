import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
fichiers_modifies = 0
fichiers_erreur = 0

# Le lien à ajouter dans la nav
lien_recherche = '<a href="recherche.html" style="text-decoration:none;color:var(--m);font-size:.82rem;font-weight:500">🔍 Rechercher</a>'

for fichier in os.listdir(dossier):
    if not fichier.endswith('.html'):
        continue
    if fichier == 'recherche.html':
        continue

    chemin = os.path.join(dossier, fichier)

    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            contenu = f.read()

        # Vérifier si le lien est déjà présent
        if 'recherche.html' in contenu:
            continue

        # Chercher la nav et ajouter le lien avant </nav>
        if '</nav>' in contenu:
            contenu = contenu.replace('</nav>', f'  {lien_recherche}\n</nav>', 1)
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(contenu)
            fichiers_modifies += 1

    except Exception as e:
        fichiers_erreur += 1
        print(f"Erreur sur {fichier}: {e}")

print(f"✅ {fichiers_modifies} fichiers modifiés")
print(f"❌ {fichiers_erreur} erreurs")
