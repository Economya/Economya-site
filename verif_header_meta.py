import glob
import re

fichiers = sorted(glob.glob('article-*.html'))

has_lecture = 0
has_verifie = 0
has_both = 0
missing_meta = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    lecture = bool(re.search(r'Lecture\s*\d', c))
    verifie = bool(re.search(r'V[ée]rifi[ée]\s*juin\s*2026', c))

    if lecture:
        has_lecture += 1
    if verifie:
        has_verifie += 1
    if lecture and verifie:
        has_both += 1
    if not lecture and not verifie:
        missing_meta.append(f)

print(f"Total articles : {len(fichiers)}")
print(f"Avec 'Lecture X min' : {has_lecture}")
print(f"Avec 'Verifie juin 2026' : {has_verifie}")
print(f"Avec les deux (ligne meta complete) : {has_both}")
print(f"SANS aucun des deux (header incomplet, ex: IA et shopping) : {len(missing_meta)}")
print()
print("Exemples de headers incomplets (10 premiers) :")
print(missing_meta[:10])
