c = open('article-226.html', encoding='utf-8').read()
idx = c.find('<footer')
print(c[max(0,idx-500):idx+400])
