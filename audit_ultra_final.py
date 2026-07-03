import re, glob

fichiers = sorted(glob.glob('article-*.html'))

# tous les noms de classe de badge connus sur le site a ce jour
NOMS_BADGE = ['savings-badge', 'saving-pill', 'hero-badge', 'abadge']

problemes = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()

    # 1. identifier quelle classe de badge est utilisee dans le HTML de ce fichier
    badge_utilise = None
    for nom in NOMS_BADGE:
        if f'class="{nom}"' in c:
            badge_utilise = nom
            break

    if not badge_utilise:
        problemes.append((f, "AUCUN BADGE CONNU TROUVE"))
        continue

    # 2. verifier si le badge a un style en ligne (garanti) OU une regle CSS avec background
    idx_badge = c.find(f'class="{badge_utilise}"')
    contexte = c[idx_badge:idx_badge+150]
    a_style_inline = 'style="' in contexte and 'background' in contexte

    style_idx = c.find('<style')
    style_end = c.find('</style>')
    style_content = c[style_idx:style_end] if style_idx != -1 else ""
    m = re.search(r'\.' + re.escape(badge_utilise) + r'\s*\{[^}]*\}', style_content)
    a_css_background = m and 'background' in m.group()

    if not (a_style_inline or a_css_background):
        problemes.append((f, f"badge {badge_utilise} sans fond (ni inline ni CSS)"))

print(f"Total articles verifies : {len(fichiers)}")
print(f"Problemes trouves : {len(problemes)}")
for f, raison in problemes:
    print(f"  {f} : {raison}")
