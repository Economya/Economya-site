c = open('article-1.html', encoding='utf-8').read()
idx = c.find('<footer')
print("Position <footer>:", idx)
print(repr(c[idx:idx+350]))
