for f in ['article-100.html', 'article-501.html']:
    c = open(f, encoding='utf-8').read()
    idx = c.find('<footer')
    print(f"=== {f} ===")
    print(repr(c[idx:idx+350]))
    print()
