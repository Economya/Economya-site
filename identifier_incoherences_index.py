import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
index_path = os.path.join(dossier, "index.html")

# Lire l'index
with open(index_path, 'r', encoding='utf-8') as f:
    index_contenu = f.read()

# Extraire toutes les cartes : href + titre affiché
cartes = re.findall(r'href="(article-\d+\.html)"[^>]*>.*?<div class="atitle">(.*?)</div>', index_contenu, re.DOTALL)

incoherences = []
coherentes = 0

for fichier, titre_carte in cartes:
    titre_carte = titre_carte.strip()
    chemin = os.path.join(dossier, fichier)
    
    if not os.path.exists(chemin):
        continue
    
    with open(chemin, 'r', encoding='utf-8') as f:
        article = f.read()
    
    # Extraire le vrai titre de l'article
    titre_match = re.search(r'<title>(.*?)</title>', article)
    if not titre_match:
        continue
    
    titre_article = titre_match.group(1).replace(' — Economya.fr', '').replace(' - Economya.fr', '').strip()
    
    # Comparer les mots clés
    mots_carte = set(re.findall(r'\b\w{4,}\b', titre_carte.lower()))
    mots_article = set(re.findall(r'\b\w{4,}\b', titre_article.lower()))
    
    if mots_carte and mots_article:
        score = len(mots_carte & mots_article) / len(mots_carte)
    else:
        score = 0
    
    if score < 0.2:
        incoherences.append({
            'fichier': fichier,
            'titre_carte': titre_carte[:50],
            'titre_article': titre_article[:50],
            'score': score
        })
    else:
        coherentes += 1

print(f"\n✅ {coherentes} cartes cohérentes")
print(f"⚠️  {len(incoherences)} cartes potentiellement incohérentes\n")
print(f"{'Fichier':<20} {'Titre carte':<45} {'Titre article'}")
print("-" * 120)
for r in incoherences:
    print(f"{r['fichier']:<20} {r['titre_carte']:<45} {r['titre_article']}")

# Sauvegarder
with open('/Users/alexandregoffinet/Desktop/mon site/incoherences_index.txt', 'w', encoding='utf-8') as f:
    f.write(f"Cartes incohérentes : {len(incoherences)}\n\n")
    for r in incoherences:
        f.write(f"{r['fichier']} | Carte: {r['titre_carte']} | Article: {r['titre_article']}\n")

print(f"\n✅ Rapport sauvegardé dans incoherences_index.txt")
