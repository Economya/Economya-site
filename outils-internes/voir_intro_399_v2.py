c = open('article-399.html', encoding='utf-8').read()
idx = c.find('Ruralité')
if idx == -1:
    idx = c.find('<title>')
print("Position trouvee:", idx)
print(c[max(0,idx-50):idx+1200])
