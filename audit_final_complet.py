import re, glob

fichiers = sorted(glob.glob('article-*.html'))
total = len(fichiers)

# 1. chercher le badge "somme" partout sur le site (pas juste les 47)
badges_somme = []
for f in fichiers:
    c = open(f, encoding='utf-8').read()
    for motif_class in ['savings-badge', 'saving-pill', 'hero-badge', 'abadge']:
        for m in re.finditer(r'class="' + motif_class + r'"[^>]*>([^<]*)</div>', c):
            texte = m.group(1)
            if 'somme' in texte.lower() or re.search(r'\b0+\s*000\s*€', texte):
                badges_somme.append((f, motif_class, texte.strip()))

print("=== BADGES CASSES (somme/chiffre tronque) ===")
for f, cls, texte in badges_somme:
    print(f"{f} ({cls}): {texte!r}")
print()

# 2. Verification finale header complet (badge present + meta present) sur TOUS les articles
NOMS_BADGE = ['savings-badge', 'saving-pill', 'hero-badge', 'abadge']
sans_badge = [f for f in fichiers if not any(n in open(f, encoding='utf-8').read() for n in NOMS_BADGE)]

r1 = re.compile(r'Lecture\s*:?\s*\d|\d\s*min\s*de\s*lecture|\d\s*min</span>|\d\s*min\s*·')
r2 = re.compile(r'V.rifi. juin 2026')
sans_meta = []
for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if not (r1.search(c) and r2.search(c)):
        sans_meta.append(f)

print(f"=== RECAP HEADER (sur {total} articles) ===")
print(f"Sans badge : {len(sans_badge)} -> {sans_badge}")
print(f"Sans ligne meta : {len(sans_meta)} -> {sans_meta}")
print()

# 3. Verification finale footer
sans_footer_pol = [f for f in fichiers if 'Politique de confidentialité' not in open(f, encoding='utf-8').read() and 'politique-confidentialite' not in open(f, encoding='utf-8').read()]
sans_partage = [f for f in fichiers if 'Partager cet article' not in open(f, encoding='utf-8').read()]
sans_nav = [f for f in fichiers if 'article-nav' not in open(f, encoding='utf-8').read() and 'test' not in f]

print(f"=== RECAP FOOTER/BAS DE PAGE (sur {total} articles) ===")
print(f"Sans lien Politique confidentialite : {len(sans_footer_pol)} -> {sans_footer_pol}")
print(f"Sans bouton Partager : {len(sans_partage)} -> {sans_partage}")
print(f"Sans nav precedent/suivant (hors doublons -test) : {len(sans_nav)} -> {sans_nav}")
