import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"

# Le CSS du menu hamburger
HAMBURGER_CSS = """
/* Menu hamburger mobile */
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:.3rem}
.hamburger span{display:block;width:24px;height:2px;background:var(--gd,#085041);border-radius:2px;transition:all .3s}
.mobile-menu{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(255,255,255,.98);z-index:999;flex-direction:column;align-items:center;justify-content:center;gap:1.5rem}
.mobile-menu.open{display:flex}
.mobile-menu a{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:#085041;text-decoration:none}
.mobile-menu .close-btn{position:absolute;top:1.2rem;right:1.5rem;background:none;border:none;font-size:1.8rem;cursor:pointer;color:#085041}
.mobile-menu .nav-cta{background:#1D9E75;color:white!important;padding:.5rem 1.4rem;border-radius:50px}
@media(max-width:768px){
  .hamburger{display:flex}
  nav .nav-links, nav > a:not(.logo), nav > div{display:none!important}
  nav li{display:none!important}
}
"""

# Le HTML du menu hamburger
HAMBURGER_HTML = """
<!-- Menu hamburger mobile -->
<button class="hamburger" onclick="toggleMenu()" aria-label="Menu">
  <span></span><span></span><span></span>
</button>
<div class="mobile-menu" id="mobileMenu">
  <button class="close-btn" onclick="toggleMenu()">✕</button>
  <a href="index.html">🏠 Accueil</a>
  <a href="jeux.html">🎮 Jeux</a>
  <a href="outils-gratuits.html">🛠️ Outils gratuits</a>
  <a href="comparateurs.html">🔍 Comparateurs</a>
  <a href="a-propos.html">ℹ️ À propos</a>
  <a href="recherche.html">🔎 Rechercher</a>
  <a href="#nl" class="nav-cta" onclick="toggleMenu()">📬 Newsletter</a>
</div>
<script>
function toggleMenu(){
  var m = document.getElementById('mobileMenu');
  m.classList.toggle('open');
  document.body.style.overflow = m.classList.contains('open') ? 'hidden' : '';
}
</script>
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip si déjà fait
    if 'hamburger' in content:
        return False

    # Ajouter le CSS avant </style>
    if '</style>' in content:
        content = content.replace('</style>', HAMBURGER_CSS + '</style>', 1)

    # Ajouter le HTML hamburger à la fin de la nav
    if '</nav>' in content:
        content = content.replace('</nav>', HAMBURGER_HTML + '</nav>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# Fichiers principaux uniquement (pas les 515 articles)
PAGES = [
    'index.html', 'jeux.html', 'outils-gratuits.html', 'comparateurs.html',
    'a-propos.html', 'mentions-legales.html', 'politique-confidentialite.html',
    'lexique-finance.html', 'recherche.html', '404.html',
    'simulateur-epargne.html', 'calculateur-budget.html', 'generateur-budget.html',
    'comparateur-livrets.html', 'checklist-abonnements.html', 'generateur-defi-epargne.html',
    'boite-economies.html', 'simulateur-credit-immo.html', 'calculateur-frais-notaire.html',
    'simulateur-apl.html', 'calculateur-capacite-emprunt.html', 'simulateur-loyer-achat.html',
    'calculateur-rendement-locatif.html', 'calculateur-salaire.html', 'calculateur-impot.html',
    'calculateur-prime-activite.html', 'simulateur-retraite.html', 'calculateur-cout-voiture.html',
    'simulateur-economies-energie.html', 'quiz-epargnant.html', 'quiz-animal-epargnant.html',
    'quiz-personnage-serie.html', 'quiz-marque.html', 'test-surconsommation.html',
    'quiz-voyageur.html', 'adn-financier.html',
    'inflation-run.html', 'le-bon-deal.html', 'le-negociateur.html', 'roue-economies.html',
    'jackpot-finance.html', 'vrai-ou-faux.html', 'finance-wrapped.html', 'aura-financiere.html',
    'investisseur-virtuel.html', 'primo-accedant.html',
]

done = 0
for page in PAGES:
    path = os.path.join(dossier, page)
    if os.path.exists(path):
        if process_file(path):
            print(f"✅ {page}")
            done += 1
    else:
        print(f"⚠️  Introuvable : {page}")

print(f"\n🎉 {done} pages mises à jour avec le menu hamburger !")
