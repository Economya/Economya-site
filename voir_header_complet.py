import re

# On cherche un article qui a le format complet (Lecture + Verifie)
import glob
fichiers = sorted(glob.glob('article-*.html'))

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if re.search(r'Lecture\s*\d', c) and re.search(r'V[ée]rifi[ée]\s*juin\s*2026', c):
        idx = c.find('Lecture')
        # on remonte un peu avant pour voir le contexte (badge categorie, titre, etc)
        print(f"=== FICHIER: {f} ===")
        print(c[max(0,idx-900):idx+400])
        break
