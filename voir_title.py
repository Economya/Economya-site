import re
for f in ['article-460.html', 'article-175.html']:
    c = open(f, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', c, re.DOTALL)
    print(f, '->', repr(m.group(1)) if m else 'PAS TROUVE')
