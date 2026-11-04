import re
c = open('article-399.html', encoding='utf-8').read()
idx = c.find('savings-badge')
print("=== Zone du badge ===")
print(c[max(0,idx-50):idx+150])
print()
# chercher le vrai montant dans le corps du texte
print("=== Recherche de montants dans les 3000 premiers caracteres du corps ===")
corps = c[idx:idx+3000]
montants = re.findall(r'\d[\d\s]{0,6}(?:€|%|\s?euros)', corps)
print(montants[:10])
