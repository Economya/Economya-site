import re
c = open('article-52.html', encoding='utf-8').read()
style_idx = c.find('<style')
style_end = c.find('</style>')
style_content = c[style_idx:style_end]

for motif in ['.article-hero', '.acat-badge', '.saving-pill', '.meta']:
    m = re.search(re.escape(motif) + r'\s*\{[^}]*\}', style_content)
    print(f"{motif} : {m.group() if m else 'PAS TROUVE'}")
