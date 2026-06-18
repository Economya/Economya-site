import os
import re

dossier = os.path.dirname(os.path.abspath(__file__))

print("Correction des liens article precedent/suivant...")
corriges = 0

for nom in os.listdir(dossier):
    if not re.match(r'article-\d+\.html', nom):
        continue
    chemin = os.path.join(dossier, nom)
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Corriger article21.html -> article-21.html (sans tiret)
    nouveau = re.sub(r'href="article(\d+)\.html"', r'href="article-\1.html"', contenu)
    
    if nouveau != contenu:
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(nouveau)
        corriges += 1

print(f"✅ {corriges} articles corrigés")
input("\nAppuyez sur Entrée pour fermer...")
