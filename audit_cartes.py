import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
index_path = os.path.join(dossier, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    index = f.read()

# Extraire toutes les cartes
cartes = re.findall(r'href="(article-\d+\.html)"[^>]*>.*?<div class="atitle">(.*?)</div>', index, re.DOTALL)

problemes = []

for fichier, titre_carte in cartes:
    titre_carte = titre_carte.strip()
    chemin = os.path.join(dossier, fichier)
    if not os.path.exists(chemin):
        continue

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    # Extraire H1 et title
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', contenu, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''
    titre = re.search(r'<title>(.*?)</title>', contenu)
    titre = titre.group(1).replace(' — Economya.fr','').strip() if titre else ''

    # Mots clés importants du titre carte
    mots_carte = set(re.findall(r'\b\w{5,}\b', titre_carte.lower()))
    mots_h1 = set(re.findall(r'\b\w{5,}\b', h1.lower()))
    mots_titre = set(re.findall(r'\b\w{5,}\b', titre.lower()))

    score = max(
        len(mots_carte & mots_h1) / len(mots_carte) if mots_carte else 0,
        len(mots_carte & mots_titre) / len(mots_carte) if mots_carte else 0
    )

    if score < 0.1:
        problemes.append({
            'fichier': fichier,
            'carte': titre_carte[:55],
            'article': (h1 or titre)[:55],
            'score': round(score, 2)
        })

print(f"\n⚠️  {len(problemes)} cartes vraiment incohérentes\n")
print(f"{'Fichier':<20} {'Titre carte':<50} {'Contenu article'}")
print("-" * 130)
for p in problemes:
    print(f"{p['fichier']:<20} {p['carte']:<50} {p['article']}")

# Sauvegarder
with open(os.path.join(dossier, 'audit_cartes.txt'), 'w', encoding='utf-8') as f:
    f.write(f"Cartes incohérentes : {len(problemes)}\n\n")
    for p in problemes:
        f.write(f"{p['fichier']} | Carte: {p['carte']} | Article: {p['article']}\n")

print(f"\n✅ Rapport dans audit_cartes.txt")
