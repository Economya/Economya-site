c = open('article-235.html', encoding='utf-8').read()
idx = c.find('<body')
print(c[idx:idx+1800])
