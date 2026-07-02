c = open('article-460.html', encoding='utf-8').read()
idx = c.find('Partager cet article')
print(c[idx-450:idx+1300])
