import re

print("=== article-108 : chercher la classe du badge lock ===")
c = open('article-108.html', encoding='utf-8').read()
idx = c.find('Protection maximale')
print(c[max(0,idx-200):idx+50])
print()

print("=== article-303 : CSS du footer ===")
c2 = open('article-303.html', encoding='utf-8').read()
style_idx = c2.find('<style')
style_end = c2.find('</style>')
style_content = c2[style_idx:style_end]
m = re.search(r'footer\s*\{[^}]*\}', style_content)
print("Regle trouvee:", m.group() if m else "AUCUNE")
idx2 = c2.find('<footer')
print(c2[idx2:idx2+300])
