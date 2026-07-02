c = open('article-105.html', encoding='utf-8').read()
idx = c.find('<body')
print(c[idx:idx+2200])
