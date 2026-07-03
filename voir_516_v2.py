c = open('article-516.html', encoding='utf-8').read()
idx = c.find('hero-cat')
print("Position de 'hero-cat':", idx)
if idx != -1:
    print(c[max(0,idx-200):idx+900])
else:
    print("meme hero-cat introuvable, on cherche 'PSYCHOLOGIE'")
    idx2 = c.find('PSYCHOLOGIE')
    print(c[max(0,idx2-300):idx2+900])
