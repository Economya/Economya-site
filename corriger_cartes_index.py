import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"
index_path = os.path.join(dossier, "index.html")

# Liste exacte des 62 articles incohérents à corriger
CORRECTIONS = {
    "article-11.html": None,
    "article-12.html": None,
    "article-13.html": None,
    "article-15.html": None,
    "article-16.html": None,
    "article-17.html": None,
    "article-18.html": None,
    "article-19.html": None,
    "article-20.html": None,
    "article-21.html": None,
    "article-22.html": None,
    "article-23.html": None,
    "article-24.html": None,
    "article-25.html": None,
    "article-109.html": None,
    "article-110.html": None,
    "article-111.html": None,
    "article-112.html": None,
    "article-113.html": None,
    "article-114.html": None,
    "article-115.html": None,
    "article-116.html": None,
    "article-117.html": None,
    "article-118.html": None,
    "article-119.html": None,
    "article-120.html": None,
    "article-165.html": None,
    "article-166.html": None,
    "article-167.html": None,
    "article-168.html": None,
    "article-169.html": None,
    "article-170.html": None,
    "article-171.html": None,
    "article-172.html": None,
    "article-173.html": None,
    "article-174.html": None,
    "article-175.html": None,
    "article-176.html": None,
    "article-177.html": None,
    "article-178.html": None,
    "article-179.html": None,
    "article-180.html": None,
    "article-181.html": None,
    "article-182.html": None,
    "article-183.html": None,
    "article-184.html": None,
    "article-185.html": None,
    "article-186.html": None,
    "article-187.html": None,
    "article-188.html": None,
    "article-189.html": None,
    "article-190.html": None,
    "article-191.html": None,
    "article-192.html": None,
    "article-193.html": None,
    "article-194.html": None,
    "article-195.html": None,
    "article-196.html": None,
    "article-197.html": None,
    "article-198.html": None,
    "article-199.html": None,
    "article-200.html": None,
}

# Lire le vrai titre de chaque article
for fichier in CORRECTIONS:
    chemin = os.path.join(dossier, fichier)
    if os.path.exists(chemin):
        with open(chemin, 'r', encoding='utf-8') as f:
            contenu = f.read()
        titre_match = re.search(r'<title>(.*?)</title>', contenu)
        if titre_match:
            titre = titre_match.group(1).replace(' — Economya.fr', '').replace(' - Economya.fr', '').strip()
            CORRECTIONS[fichier] = titre

# Lire l'index
with open(index_path, 'r', encoding='utf-8') as f:
    index = f.read()

corriges = 0

for fichier, nouveau_titre in CORRECTIONS.items():
    if not nouveau_titre:
        continue
    
    # Pattern exact : trouver la carte avec ce fichier et remplacer son atitle
    pattern = r'(href="' + re.escape(fichier) + r'".*?<div class="atitle">)(.*?)(</div>)'
    
    def remplacer(m):
        global corriges
        corriges += 1
        return m.group(1) + nouveau_titre + m.group(3)
    
    index = re.sub(pattern, remplacer, index, flags=re.DOTALL)

# Sauvegarder
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index)

print(f"✅ {corriges} cartes corrigées")
print(f"❌ {len(CORRECTIONS) - corriges} cartes non trouvées")
