import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"

# Liens affiliés
HOMESERVE_LINK = "https://www.awin1.com/cread.php?awinmid=30641&awinaffid=2926395&ued=https%3A%2F%2Fwww.homeserve.fr"
SHARESUB_LINK = "https://www.awin1.com/cread.php?awinmid=124748&awinaffid=2926395&ued=https%3A%2F%2Fwww.sharesub.com"
FUNDORA_LINK = "https://www.awin1.com/cread.php?awinmid=124808&awinaffid=2926395&ued=https%3A%2F%2Fwww.fundora.fr"

# Bannières HTML
BANNER_HOMESERVE = f'''
<!-- Partenaire HomeServe -->
<div style="background:linear-gradient(135deg,#E1F5EE,#f0fdf4);border:1px solid #1D9E75;border-radius:16px;padding:1.2rem 1.5rem;margin:2rem 0;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
  <span style="font-size:2rem">🔧</span>
  <div style="flex:1;min-width:200px">
    <div style="font-weight:700;color:#085041;font-size:.95rem;margin-bottom:.2rem">Protégez votre logement avec HomeServe</div>
    <div style="font-size:.82rem;color:#5F5E5A">Contrats d'assistance plomberie, électricité, chauffage. Intervention rapide 24h/24.</div>
  </div>
  <a href="{HOMESERVE_LINK}" target="_blank" rel="noopener sponsored" style="background:#1D9E75;color:white;padding:.6rem 1.2rem;border-radius:50px;font-weight:700;font-size:.82rem;text-decoration:none;white-space:nowrap">Découvrir →</a>
</div>
<!-- Fin partenaire -->'''

BANNER_SHARESUB = f'''
<!-- Partenaire Sharesub -->
<div style="background:linear-gradient(135deg,#EDE7F6,#f5f0ff);border:1px solid #7c3aed;border-radius:16px;padding:1.2rem 1.5rem;margin:2rem 0;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
  <span style="font-size:2rem">📺</span>
  <div style="flex:1;min-width:200px">
    <div style="font-weight:700;color:#4c1d95;font-size:.95rem;margin-bottom:.2rem">Partagez vos abonnements légalement avec Sharesub</div>
    <div style="font-size:.82rem;color:#5F5E5A">Netflix, Spotify, Disney+... Divisez vos abonnements par 2, 3 ou 4 légalement.</div>
  </div>
  <a href="{SHARESUB_LINK}" target="_blank" rel="noopener sponsored" style="background:#7c3aed;color:white;padding:.6rem 1.2rem;border-radius:50px;font-weight:700;font-size:.82rem;text-decoration:none;white-space:nowrap">Essayer →</a>
</div>
<!-- Fin partenaire -->'''

BANNER_FUNDORA = f'''
<!-- Partenaire Fundora -->
<div style="background:linear-gradient(135deg,#FAEEDA,#FFF8EE);border:1px solid #EF9F27;border-radius:16px;padding:1.2rem 1.5rem;margin:2rem 0;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
  <span style="font-size:2rem">💰</span>
  <div style="flex:1;min-width:200px">
    <div style="font-weight:700;color:#633806;font-size:.95rem;margin-bottom:.2rem">Faites fructifier votre épargne avec Fundora</div>
    <div style="font-size:.82rem;color:#5F5E5A">Investissez facilement dans des projets rentables. Commencez dès 100€.</div>
  </div>
  <a href="{FUNDORA_LINK}" target="_blank" rel="noopener sponsored" style="background:#EF9F27;color:white;padding:.6rem 1.2rem;border-radius:50px;font-weight:700;font-size:.82rem;text-decoration:none;white-space:nowrap">Investir →</a>
</div>
<!-- Fin partenaire -->'''

# Articles cibles par affilié
HOMESERVE_ARTICLES = [
    "article-9.html",   # Loyer
    "article-20.html",  # Meubler appartement
    "article-54.html",  # Panneaux solaires
    "article-110.html", # Réduire facture électricité
    "article-70.html",  # Ménage à domicile
    "article-116.html", # Relooker ses meubles
    "article-118.html", # Créer son site (maison)
    "article-350.html", # Parkings et caves
    "article-510.html", # Renégocier crédit immo
    "article-511.html", # Airbnb
]

SHARESUB_ARTICLES = [
    "article-13.html",  # Netflix Spotify
    "article-141.html", # Logiciels gratuits
    "article-250.html", # VPN
    "article-188.html", # Boxes abonnements
    "article-143.html", # Soirées apéros
    "article-502.html", # IA et shopping
    "article-504.html", # Vinted
]

FUNDORA_ARTICLES = [
    "article-101.html", # Psychologie argent
    "article-100.html", # Plan d'action économies
    "article-350.html", # Parkings investissement
    "article-509.html", # Inflation pouvoir d'achat
    "article-514.html", # Investir inflation
    "article-510.html", # Crédit immo
    "article-512.html", # SCI
]

def integrer_banniere(fichier, banniere, nom):
    chemin = os.path.join(dossier, fichier)
    if not os.path.exists(chemin):
        print(f"⚠️ Introuvable : {fichier}")
        return False
    
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Vérifier si déjà intégré
    if nom in contenu:
        print(f"⏭️ Déjà intégré : {fichier}")
        return False
    
    # Insérer avant le footer
    if '</div>\n\n<footer' in contenu:
        contenu = contenu.replace('</div>\n\n<footer', banniere + '\n</div>\n\n<footer')
    elif '</div>\n<footer' in contenu:
        contenu = contenu.replace('</div>\n<footer', banniere + '\n</div>\n<footer')
    else:
        # Insérer avant </body>
        contenu = contenu.replace('</body>', banniere + '\n</body>')
    
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)
    return True

print("🔧 Intégration HomeServe...")
hs_count = 0
for article in HOMESERVE_ARTICLES:
    if integrer_banniere(article, BANNER_HOMESERVE, 'HomeServe'):
        print(f"  ✅ {article}")
        hs_count += 1

print(f"\n📺 Intégration Sharesub...")
ss_count = 0
for article in SHARESUB_ARTICLES:
    if integrer_banniere(article, BANNER_SHARESUB, 'Sharesub'):
        print(f"  ✅ {article}")
        ss_count += 1

print(f"\n💰 Intégration Fundora...")
fd_count = 0
for article in FUNDORA_ARTICLES:
    if integrer_banniere(article, BANNER_FUNDORA, 'Fundora'):
        print(f"  ✅ {article}")
        fd_count += 1

total = hs_count + ss_count + fd_count
print(f"\n🎉 Terminé ! {total} articles mis à jour")
print(f"   HomeServe : {hs_count} articles")
print(f"   Sharesub  : {ss_count} articles")
print(f"   Fundora   : {fd_count} articles")
