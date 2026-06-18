import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
index_path = os.path.join(dossier, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    index = f.read()

corriges = 0
ignores = 0

# Trouver tous les liens d'articles dans l'index
fichiers = re.findall(r'href="(article-\d+\.html)"', index)
fichiers = list(dict.fromkeys(fichiers))  # dédoublonner

for fichier in fichiers:
    chemin = os.path.join(dossier, fichier)
    if not os.path.exists(chemin):
        ignores += 1
        continue

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    # Extraire le vrai titre — d'abord H1, sinon title
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', contenu, re.DOTALL)
    if h1:
        vrai_titre = re.sub(r'<[^>]+>', '', h1.group(1)).strip()
    else:
        titre = re.search(r'<title>(.*?)</title>', contenu)
        if not titre:
            ignores += 1
            continue
        vrai_titre = titre.group(1).replace(' — Economya.fr', '').replace(' - Economya.fr', '').strip()

    if not vrai_titre:
        ignores += 1
        continue

    # Trouver la carte dans l'index et remplacer son atitle
    pattern = r'(href="' + re.escape(fichier) + r'"[^>]*>.*?<div class="atitle">)(.*?)(</div>)'
    match = re.search(pattern, index, re.DOTALL)
    
    if match:
        titre_actuel = match.group(2).strip()
        if titre_actuel != vrai_titre:
            old = match.group(1) + match.group(2) + match.group(3)
            new = match.group(1) + vrai_titre + match.group(3)
            index = index.replace(old, new, 1)
            corriges += 1

# Sauvegarder
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index)

print(f"✅ {corriges} cartes synchronisées")
print(f"⏭️  {ignores} articles ignorés (introuvables)")
print(f"\n🎉 Index synchronisé avec tous les articles !")
