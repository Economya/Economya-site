c = open('article-52.html', encoding='utf-8').read()
idx = c.find('</script>')
# on cherche apres le premier json-ld
idx2 = c.find('</script>', idx+1)
print(c[idx2:idx2+1200])
