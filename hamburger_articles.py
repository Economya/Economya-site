import os
import re

dossier = "/Users/alexandregoffinet/Desktop/mon site"

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
  nav .nav-links,nav > a:not(.logo),nav > div{display:none!important}
  nav li{display:none!important}
}
"""

HAMBURGER_HTML = """
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
  <a href="index.html#nl" class="nav-cta" onclick="toggleMenu()">📬 Newsletter</a>
</div>
<script>
function toggleMenu(){
  var m=document.getElementById('mobileMenu');
  m.classList.toggle('open');
  document.body.style.overflow=m.classList.contains('open')?'hidden':'';
}
</script>
"""

done = 0
skipped = 0
errors = 0

for i in range(1, 516):
    fichier = f"article-{i}.html"
    chemin = os.path.join(dossier, fichier)
    
    if not os.path.exists(chemin):
        continue
    
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'hamburger' in content:
            skipped += 1
            continue
        
        if '</style>' in content:
            content = content.replace('</style>', HAMBURGER_CSS + '</style>', 1)
        
        if '</nav>' in content:
            content = content.replace('</nav>', HAMBURGER_HTML + '</nav>', 1)
        
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(content)
        
        done += 1
        
    except Exception as e:
        errors += 1

print(f"✅ {done} articles mis à jour")
print(f"⏭️  {skipped} déjà faits")
print(f"❌ {errors} erreurs")
print(f"\n🎉 Menu hamburger ajouté sur les 515 articles !")
