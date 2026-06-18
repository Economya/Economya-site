import os
import re

dossier = os.path.dirname(os.path.abspath(__file__))
fichier = os.path.join(dossier, 'index.html')

with open(fichier, 'r', encoding='utf-8') as f:
    contenu = f.read()

nb = len(re.findall(r'href="articles\.html#a\d+"', contenu))
nouveau = re.sub(r'href="articles\.html#a(\d+)"', r'href="article-\1.html"', contenu)

with open(fichier, 'w', encoding='utf-8') as f:
    f.write(nouveau)

print(f"✅ {nb} liens corrigés dans index.html")
print("✅ articles.html#a1 → article-1.html etc.")
input("\nAppuyez sur Entrée pour fermer...")
