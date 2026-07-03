import glob

fichiers = sorted(glob.glob('article-*.html'))
casses = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if ': root{' in c or ': root {' in c:
        casses.append(f)

print(f"Total articles : {len(fichiers)}")
print(f"Articles avec le bug ': root' (espace en trop, CSS invalide) : {len(casses)}")
print(casses)
