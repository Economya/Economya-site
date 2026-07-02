import re

# variante A (431 articles) - exemple
c1 = open('article-460.html', encoding='utf-8').read()
idx1 = c1.find('<footer>')
print("=== VARIANTE A (article-460, 'Fait avec coeur') ===")
print(c1[idx1:idx1+500])
print()

# variante B (98 articles) - exemple
c2 = open('article-175.html', encoding='utf-8').read()
idx2 = c2.find('<footer>')
print("=== VARIANTE B (article-175, 'Retour a l accueil') ===")
print(c2[idx2:idx2+500])
