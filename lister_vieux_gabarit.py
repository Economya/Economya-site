import glob, re

fichiers = sorted(glob.glob('article-*.html'))
old_hero_re = re.compile(r'class="hero"')
new_hero_re = re.compile(r'class="article-hero"')

resultats = []
for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if old_hero_re.search(c) and not new_hero_re.search(c):
        m = re.search(r'<title>(.*?)</title>', c, re.DOTALL)
        titre = m.group(1).strip() if m else '?'
        resultats.append((f, titre))

print(f"{len(resultats)} articles au vieux gabarit :\n")
for f, titre in resultats:
    print(f"{f:25s} -> {titre}")
