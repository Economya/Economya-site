import re, glob

fichiers = sorted(glob.glob('article-*.html'))

NOMS_BADGE = ['savings-badge', 'saving-pill', 'hero-badge', 'abadge']

badges_sans_fond = []
footer_sans_fond = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    style_idx = c.find('<style')
    style_end = c.find('</style>')
    style_content = c[style_idx:style_end] if style_idx != -1 else ""

    # Quel nom de badge est utilise dans le HTML de CETTE page
    badge_utilise = None
    for nom in NOMS_BADGE:
        if f'class="{nom}"' in c:
            badge_utilise = nom
            break

    if badge_utilise:
        m = re.search(r'\.' + re.escape(badge_utilise) + r'\s*\{[^}]*\}', style_content)
        a_fond = m and 'background' in m.group()
        if not a_fond:
            badges_sans_fond.append((f, badge_utilise))

    # Footer : cherche une regle CSS "footer{...background...}"
    m2 = re.search(r'footer\s*\{[^}]*\}', style_content)
    a_fond_footer = m2 and 'background' in m2.group()
    if not a_fond_footer:
        footer_sans_fond.append(f)

print(f"Total articles : {len(fichiers)}")
print()
print(f"BADGES sans fond CSS : {len(badges_sans_fond)}")
for f, nom in badges_sans_fond[:40]:
    print(f"  {f} (classe: {nom})")
print()
print(f"FOOTER sans fond CSS : {len(footer_sans_fond)}")
for f in footer_sans_fond[:40]:
    print(f"  {f}")
