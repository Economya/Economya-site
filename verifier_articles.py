import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
resultats = []

for fichier in sorted(os.listdir(dossier)):
    if not fichier.startswith('article-') or not fichier.endswith('.html'):
        continue

    chemin = os.path.join(dossier, fichier)

    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            contenu = f.read()

        # Extraire le titre
        titre_match = re.search(r'<title>(.*?)</title>', contenu)
        titre = titre_match.group(1) if titre_match else ''
        titre = titre.replace(' — Economya.fr', '').replace(' - Economya.fr', '').strip().lower()

        # Extraire le premier paragraphe de contenu
        para_match = re.search(r'<p[^>]*>(.*?)</p>', contenu, re.DOTALL)
        premier_para = para_match.group(1) if para_match else ''
        premier_para = re.sub(r'<[^>]+>', '', premier_para).strip().lower()

        # Extraire les mots clés du titre
        mots_titre = set(re.findall(r'\b\w{4,}\b', titre))
        mots_para = set(re.findall(r'\b\w{4,}\b', premier_para))

        # Vérifier combien de mots du titre sont dans le premier paragraphe
        if mots_titre:
            intersection = mots_titre & mots_para
            score = len(intersection) / len(mots_titre)
        else:
            score = 0

        if score < 0.2:  # Moins de 20% de mots en commun = probablement incohérent
            resultats.append({
                'fichier': fichier,
                'titre': titre[:60],
                'score': score,
                'para': premier_para[:80]
            })

    except Exception as e:
        print(f"Erreur sur {fichier}: {e}")

# Afficher les résultats
print(f"\n⚠️  {len(resultats)} articles potentiellement incohérents détectés\n")
print(f"{'Fichier':<20} {'Score':<8} {'Titre':<40} {'Début contenu'}")
print("-" * 120)
for r in resultats[:50]:  # Afficher les 50 premiers
    print(f"{r['fichier']:<20} {r['score']:.2f}     {r['titre'][:40]:<40} {r['para'][:60]}")

# Sauvegarder la liste complète
with open('/Users/alexandregoffinet/Desktop/mon site/articles_incoherents.txt', 'w', encoding='utf-8') as f:
    f.write(f"Articles potentiellement incohérents : {len(resultats)}\n\n")
    for r in resultats:
        f.write(f"{r['fichier']} | Score: {r['score']:.2f} | Titre: {r['titre']}\n")

print(f"\n✅ Liste complète sauvegardée dans articles_incoherents.txt")
