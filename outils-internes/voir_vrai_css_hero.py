import re

c = open('article-1.html', encoding='utf-8').read()

style_idx = c.find('<style')
style_end = c.find('</style>')
style_content = c[style_idx:style_end] if style_idx != -1 else ""

for motif in ['.article-hero', '.article-cat', '.savings-badge', '.article-meta', '.intro-box']:
    m = re.search(re.escape(motif) + r'\s*\{[^}]*\}', style_content)
    if m:
        print(f"=== {motif} ===")
        print(m.group())
        print()
    else:
        print(f"=== {motif} : NON TROUVE ===")
        print()
