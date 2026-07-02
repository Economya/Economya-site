for f in ['article-501.html', 'article-500.html']:
    c = open(f, encoding='utf-8').read()
    idx = c.find('class="hero"')
    print(f"=== {f} ===")
    if idx == -1:
        print("PAS DE class=\"hero\" TROUVE DU TOUT")
        idx2 = c.find('<body')
        print(c[idx2:idx2+900])
    else:
        print(c[max(0,idx-30):idx+700])
    print()
