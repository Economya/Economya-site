import re, glob
fichiers = sorted(glob.glob('article-*.html'))
NOMS_BADGE = ['savings-badge', 'saving-pill', 'hero-badge', 'abadge']
vrais_sans_badge = [f for f in fichiers if not any(n in open(f, encoding='utf-8').read() for n in NOMS_BADGE)]
print("SANS BADGE:", len(vrais_sans_badge), vrais_sans_badge)
r1 = re.compile(r'Lecture\s*:?\s*\d|\d\s*min\s*de\s*lecture|\d\s*min</span>')
r2 = re.compile(r'V.rifi. juin 2026')
vrais_sans_meta = []
for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if not (r1.search(c) and r2.search(c)):
        vrais_sans_meta.append(f)
print("SANS META:", len(vrais_sans_meta), vrais_sans_meta)
