c = open('article-132.html', encoding='utf-8').read()
idx = c.find('<body')
print(c[idx:idx+2000])
