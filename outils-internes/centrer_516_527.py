import re, shutil

FICHIERS = [f"article-{i}.html" for i in range(516, 528)]

PATTERN = re.compile(
    r'<div class="hero">(.*?)</div>\s*(?=<div class="container"|<article|<div class="ab")',
    re.DOTALL
)

def centrer_enfants(inner_html):
    inner_html = re.sub(
        r'<div class="hero-cat">',
        '<div class="hero-cat" style="display:inline-block;margin:0 auto 1rem">',
        inner_html
    )
    inner_html = re.sub(
        r'<h1>',
        '<h1 style="text-align:center">',
        inner_html
    )
    inner_html = re.sub(
        r'<div class="hero-badge">',
        '<div class="hero-badge" style="display:inline-block;margin:1rem auto">',
        inner_html
    )
    inner_html = re.sub(
        r'<div class="hero-meta"[^>]*>',
        '<div class="hero-meta" style="display:flex;justify-content:center;'
        'align-items:center;flex-wrap:wrap;gap:1rem;text-align:center;'
        'width:100%;margin-top:.8rem">',
        inner_html
    )
    return inner_html

traites = 0
for f in FICHIERS:
    try:
        c = open(f, encoding='utf-8').read()
    except FileNotFoundError:
        print(f"introuvable: {f}")
        continue

    if 'data-hero-centered="1"' in c:
        print(f"deja centre: {f}")
        continue

    m = PATTERN.search(c)
    if not m:
        print(f"structure non reconnue: {f}")
        continue

    inner = centrer_enfants(m.group(1))
    nouveau_bloc = (
        '<div class="hero" data-hero-centered="1" '
        'style="text-align:center;display:flex;flex-direction:column;'
        'align-items:center">'
        f'{inner}</div>'
    )
    c_new = c[:m.start()] + nouveau_bloc + c[m.end():]

    shutil.copy2(f, f + '.bak_centrage2')
    open(f, 'w', encoding='utf-8').write(c_new)
    print(f"OK {f} : centre")
    traites += 1

print(f"\nTotal traite: {traites}")
