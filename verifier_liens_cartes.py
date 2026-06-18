import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
index_path = os.path.join(dossier, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    index = f.read()

# Extraire toutes les cartes : href + titre carte + titre article réel
pattern = r'href="(article-\d+\.html)"[^>]*>.*?<div class="atitle">(.*?)</div>'
cartes = re.findall(pattern, index, re.DOTALL)

incoherences = []
coherentes = 0

for fichier, titre_carte in cartes:
    titre_carte = titre_carte.strip()
    chemin = os.path.join(dossier, fichier)
    
    if not os.path.exists(chemin):
        continue
    
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Extraire le vrai titre de l'article
    titre_match = re.search(r'<title>(.*?)</title>', contenu)
    if not titre_match:
        continue
    titre_article = titre_match.group(1).replace(' — Economya.fr', '').strip()
    
    # Extraire aussi le h1 de l'article
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', contenu, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''

    # Comparer mots clés carte vs titre article
    mots_carte = set(re.findall(r'\b\w{4,}\b', titre_carte.lower()))
    mots_article = set(re.findall(r'\b\w{4,}\b', titre_article.lower()))
    mots_h1 = set(re.findall(r'\b\w{4,}\b', h1.lower()))
    
    score_titre = len(mots_carte & mots_article) / len(mots_carte) if mots_carte else 0
    score_h1 = len(mots_carte & mots_h1) / len(mots_carte) if mots_carte else 0
    score = max(score_titre, score_h1)
    
    if score < 0.15:
        incoherences.append({
            'fichier': fichier,
            'titre_carte': titre_carte[:50],
            'titre_article': titre_article[:50],
            'score': score
        })
    else:
        coherentes += 1

print(f"\n✅ {coherentes} cartes cohérentes")
print(f"⚠️  {len(incoherences)} cartes incohérentes (mauvais lien href)\n")
print(f"{'Fichier':<20} {'Titre carte':<45} {'Vrai titre article'}")
print("-" * 120)
for r in incoherences:
    print(f"{r['fichier']:<20} {r['titre_carte']:<45} {r['titre_article']}")

# Sauvegarder
with open(os.path.join(dossier, 'liens_incoherents.txt'), 'w', encoding='utf-8') as f:
    f.write(f"Cartes avec mauvais liens : {len(incoherences)}\n\n")
    for r in incoherences:
        f.write(f"{r['fichier']} | Carte: {r['titre_carte']} | Article: {r['titre_article']}\n")

print(f"\n✅ Rapport sauvegardé dans liens_incoherents.txt")
