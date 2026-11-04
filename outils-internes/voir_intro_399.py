import re
c = open('article-399.html', encoding='utf-8').read()
idx = c.find('<h1>')
print(c[idx:idx+900])
