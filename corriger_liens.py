import os
import re

dossier = os.path.dirname(os.path.abspath(__file__))
fichier = os.path.join(dossier, 'index.html')

with open(fichier, 'r', encoding='utf-8') as f:
    contenu = f.read()

# Remplacer href='/article-XXX' par href='article-XXX.html'
# Pattern: href='/article-NNN' sans .html
nouveau = re.sub(r"href='/article-(\d+)'", r"href='article-\1.html'", contenu)

# Compter les remplacements
nb = len(re.findall(r"href='/article-\d+'", contenu))

with open(fichier, 'w', encoding='utf-8') as f:
    f.write(nouveau)

print(f"✅ {nb} liens corrigés dans index.html")
print(f"✅ Les articles 201-500 sont maintenant bien liés")
input("\nAppuyez sur Entrée pour fermer...")
