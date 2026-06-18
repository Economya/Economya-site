import os

dossier = "/Users/alexandregoffinet/Desktop/mon site"

# Liste des 47 articles incohérents détectés
articles_a_supprimer = [
    "article-100.html", "article-101.html", "article-105.html", "article-110.html",
    "article-117.html", "article-12.html", "article-121.html", "article-122.html",
    "article-129.html", "article-13.html", "article-131.html", "article-136.html",
    "article-141.html", "article-143.html", "article-155.html", "article-16.html",
    "article-161.html", "article-179.html", "article-18.html", "article-20.html",
    "article-236.html", "article-239.html", "article-250.html", "article-259.html",
    "article-294.html", "article-30.html", "article-301.html", "article-31.html",
    "article-35.html", "article-350.html", "article-359.html", "article-36.html",
    "article-397.html", "article-399.html", "article-407.html", "article-42.html",
    "article-476.html", "article-482.html", "article-54.html", "article-61.html",
    "article-70.html", "article-78.html", "article-79.html", "article-84.html",
    "article-9.html", "article-90.html", "article-95.html"
]

supprimes = 0
erreurs = 0

for fichier in articles_a_supprimer:
    chemin = os.path.join(dossier, fichier)
    try:
        if os.path.exists(chemin):
            os.remove(chemin)
            supprimes += 1
            print(f"🗑️ Supprimé : {fichier}")
        else:
            print(f"⚠️ Introuvable : {fichier}")
    except Exception as e:
        erreurs += 1
        print(f"❌ Erreur sur {fichier}: {e}")

print(f"\n✅ {supprimes} articles supprimés")
print(f"❌ {erreurs} erreurs")
print(f"📊 Il reste {500 - supprimes} articles dans le dossier")
