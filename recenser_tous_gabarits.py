import glob, re

fichiers = sorted(glob.glob('article-*.html'))
gabarits = {}

# on cherche tout div dont la classe contient "hero"
pattern = re.compile(r'<div class="([^"]*hero[^"]*)"')

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    m = pattern.search(c)
    cle = m.group(1) if m else "AUCUN_HERO_TROUVE"
    gabarits.setdefault(cle, []).append(f)

print(f"{len(gabarits)} gabarits differents trouves sur {len(fichiers)} articles\n")
for cle, files in sorted(gabarits.items(), key=lambda x: -len(x[1])):
    print(f'"{cle}"  ->  {len(files)} articles  (ex: {files[0]})')
