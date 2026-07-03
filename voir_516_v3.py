c = open('article-516.html', encoding='utf-8').read()
idx = c.find('<div class="hero-cat">')
print("Position du vrai HTML 'hero-cat' (avec div class=):", idx)
if idx != -1:
    print(c[max(0,idx-100):idx+900])
else:
    idx2 = c.find('<body')
    print("Fallback, debut du body:")
    print(c[idx2:idx2+1500])
