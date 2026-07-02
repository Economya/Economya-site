c = open('article-201.html', encoding='utf-8').read()
idx = c.find('class="hero"')
print(c[max(0,idx-30):idx+700])
