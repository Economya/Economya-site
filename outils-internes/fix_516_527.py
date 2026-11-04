import re, shutil

FICHIERS = [f"article-{i}.html" for i in range(516, 528)]

def calc_lecture(texte):
    mots = len(re.findall(r'\w+', texte))
    return max(2, round(mots / 200))

PATTERN = re.compile(r'(<div class="hero-badge">.*?</div>)(\s*</div>)', re.DOTALL)

traites = 0
for f in FICHIERS:
    try:
        c = open(f, encoding='utf-8').read()
    except FileNotFoundError:
        print(f"introuvable: {f}")
        continue
    if 'hero-meta' in c:
        print(f"deja bon: {f}")
        continue
    m = PATTERN.search(c)
    if not m:
        print(f"structure non reconnue: {f}")
        continue
    texte_brut = re.sub(r'<[^>]+>', ' ', c)
    minutes = calc_lecture(texte_brut)
    meta_html = (
        '<div class="hero-meta" style="display:flex;justify-content:center;'
        'align-items:center;flex-wrap:wrap;gap:1rem;text-align:center;'
        'width:100%;margin-top:.8rem">'
        f'<span>Lecture {minutes} min</span>'
        '<span>Verifie juin 2026</span>'
        '<span>Adapte au marche francais</span>'
        '</div>'
    )
    c_new = c[:m.end(1)] + meta_html + c[m.end(1):]
    shutil.copy2(f, f + '.bak_meta1216')
    open(f, 'w', encoding='utf-8').write(c_new)
    print(f"OK {f} : {minutes} min")
    traites += 1

print(f"\nTotal traite: {traites}")
