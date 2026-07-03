import re

c = open('article-399.html', encoding='utf-8').read()
idx = c.find('savings-badge')
print("=== Contexte du badge ===")
print(c[max(0,idx-50):idx+150])
print()

# chercher tous les montants dans les 3000 premiers caracteres du corps
idx_body = c.find('<div class="content"')
if idx_body == -1:
    idx_body = c.find('<article')
corps = c[idx_body:idx_body+3000] if idx_body != -1 else c[idx:idx+3000]
montants = re.findall(r'\d[\d\s]{0,7}(?:€|%|\s?euros)', corps)
print("=== Montants trouves dans le corps de l'article ===")
print(montants[:15])
