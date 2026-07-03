c = open('article-52.html', encoding='utf-8').read()
idx = c.find('<h1')
print(c[max(0,idx-300):idx+800])
