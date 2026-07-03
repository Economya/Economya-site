c = open('article-516.html', encoding='utf-8').read()
idx = c.find('<div class="hero">')
print(c[idx:idx+1200])
