import re, glob

fichiers = sorted(glob.glob('article-*.html'))
total = len(fichiers)

sans_politique_conf = []
sans_nav = []
sans_savings_badge = []
sans_meta_row = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if 'Politique de confidentialité' not in c and 'politique-confidentialite' not in c:
        sans_politique_conf.append(f)
    if 'article-nav' not in c and 'Article précédent' not in c and 'Article suivant' not in c:
        sans_nav.append(f)
    if 'savings-badge' not in c:
        sans_savings_badge.append(f)
    a_lecture = bool(re.search(r'Lecture\s*:?\s*\d|\d\s*min\s*de\s*lecture', c))
    a_verifie = bool(re.search(r'V[ée]rifi[ée]\s*juin\s*2026', c))
    if not (a_lecture and a_verifie):
        sans_meta_row.append(f)

print(f"Total articles : {total}")
print()
print(f"Sans lien Politique de confidentialite dans le footer : {len(sans_politique_conf)}")
print(sans_politique_conf[:15])
print()
print(f"Sans nav precedent/suivant : {len(sans_nav)}")
print(sans_nav[:15])
print()
print(f"Sans savings-badge : {len(sans_savings_badge)}")
print(sans_savings_badge[:15])
print()
print(f"Sans ligne meta complete (Lecture + Verifie) : {len(sans_meta_row)}")
print(sans_meta_row[:15])
