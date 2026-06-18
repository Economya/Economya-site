import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"

ANYVAN_LINK = "https://www.awin1.com/cread.php?awinmid=126967&awinaffid=2926395&ued=https%3A%2F%2Fwww.anyvan.com%2Ffr"

BANNER_ANYVAN = f'''
<!-- Partenaire AnyVan -->
<div style="background:linear-gradient(135deg,#EEF2FF,#E0E7FF);border:1px solid #6366f1;border-radius:16px;padding:1.2rem 1.5rem;margin:2rem 0;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
  <span style="font-size:2rem">🚚</span>
  <div style="flex:1;min-width:200px">
    <div style="font-weight:700;color:#3730a3;font-size:.95rem;margin-bottom:.2rem">Déménagez moins cher avec AnyVan</div>
    <div style="font-size:.82rem;color:#5F5E5A">Comparez les transporteurs et économisez jusqu'à 75% sur votre déménagement. Devis gratuit en 2 minutes.</div>
  </div>
  <a href="{ANYVAN_LINK}" target="_blank" rel="noopener sponsored" style="background:#6366f1;color:white;padding:.6rem 1.2rem;border-radius:50px;font-weight:700;font-size:.82rem;text-decoration:none;white-space:nowrap">Devis gratuit →</a>
</div>
<!-- Fin partenaire -->'''

ANYVAN_ARTICLES = [
    "article-399.html",  # Ruralité / quitter la ville
    "article-511.html",  # Airbnb / logement
    "article-510.html",  # Crédit immo
    "article-512.html",  # SCI / immobilier
    "article-9.html",    # Loyer
    "article-20.html",   # Meubler appartement
    "article-116.html",  # Relooker meubles
    "article-350.html",  # Parkings et caves
    "article-507.html",  # Télétravailler Portugal
    "article-508.html",  # Nomade digital
]

def integrer_banniere(fichier, banniere, nom):
    chemin = os.path.join(dossier, fichier)
    if not os.path.exists(chemin):
        print(f"⚠️ Introuvable : {fichier}")
        return False
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if nom in contenu:
        print(f"⏭️ Déjà intégré : {fichier}")
        return False
    if '</div>\n\n<footer' in contenu:
        contenu = contenu.replace('</div>\n\n<footer', banniere + '\n</div>\n\n<footer')
    elif '</div>\n<footer' in contenu:
        contenu = contenu.replace('</div>\n<footer', banniere + '\n</div>\n<footer')
    else:
        contenu = contenu.replace('</body>', banniere + '\n</body>')
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)
    return True

print("🚚 Intégration AnyVan...")
count = 0
for article in ANYVAN_ARTICLES:
    if integrer_banniere(article, BANNER_ANYVAN, 'AnyVan'):
        print(f"  ✅ {article}")
        count += 1

print(f"\n🎉 {count} articles mis à jour avec AnyVan !")
