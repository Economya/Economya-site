import glob

fichiers = sorted(glob.glob('article-*.html'))
problemes = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    ouvrants = c.count('<div')
    fermants = c.count('</div>')
    if ouvrants != fermants:
        problemes.append((f, ouvrants, fermants, ouvrants - fermants))

print(f"Total articles : {len(fichiers)}")
print(f"Articles avec desequilibre <div>/</div> : {len(problemes)}")
print()
for f, o, fe, diff in problemes:
    print(f"  {f} : {o} ouvrants, {fe} fermants (ecart: {diff:+d})")
