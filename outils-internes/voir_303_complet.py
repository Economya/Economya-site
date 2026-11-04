c = open('article-303.html', encoding='utf-8').read()
idx = c.find('<footer')
print(repr(c[idx:idx+700]))
