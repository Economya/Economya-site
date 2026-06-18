import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
index_path = os.path.join(dossier, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    index = f.read()

pattern = r'(href="(article-\d+\.html)"[^>]*>.*?<div class="atitle">)(.*?)(</div>)'
cartes = re.findall(pattern, index, re.DOTALL)

corriges = 0

for full_before, fichier, titre_carte, closing in cartes:
    titre_carte = titre_carte.strip()
    chemin = os.path.join(dossier, fichier)
    if not os.path.exists(chemin):
        continue

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    # Vrai titre de l'article
    titre_match = re.search(r'<title>(.*?)</title>', contenu)
    if not titre_match:
        continue
    titre_article = titre_match.group(1).replace(' — Economya.fr', '').replace(' - Economya.fr', '').strip()

    # Comparer
    mots_carte = set(re.findall(r'\b\w{4,}\b', titre_carte.lower()))
    mots_article = set(re.findall(r'\b\w{4,}\b', titre_article.lower()))
    score = len(mots_carte & mots_article) / len(mots_carte) if mots_carte else 0

    if score < 0.15:
        # Remplacer le titre de la carte par le vrai titre
        old = full_before + titre_carte + closing
        new = full_before + titre_article + closing
        if old in index:
            index = index.replace(old, new, 1)
            corriges += 1
            print(f"✅ {fichier}")
            print(f"   Avant : {titre_carte[:50]}")
            print(f"   Après : {titre_article[:50]}")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index)

print(f"\n🎉 {corriges} cartes corrigées !")
