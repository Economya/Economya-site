import os

hamburger_css = """
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:.3rem}
.hamburger span{display:block;width:24px;height:2px;background:var(--gd,#085041);border-radius:2px;transition:all .3s}
.mobile-menu{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(255,255,255,.98);z-index:999;flex-direction:column;align-items:center;justify-content:center;gap:1.5rem}
.mobile-menu.open{display:flex}
.mobile-menu a{font-size:1.3rem;font-weight:700;color:#085041;text-decoration:none}
.mobile-menu .close-btn{position:absolute;top:1.2rem;right:1.5rem;background:none;border:none;font-size:1.8rem;cursor:pointer;color:#085041}
.mobile-menu .nav-cta{background:#1D9E75;color:white;padding:.5rem 1.4rem;border-radius:50px}
@media(max-width:768px){.hamburger{display:flex}nav ul{display:none}}"""

hamburger_html = """
<button class="hamburger" onclick="toggleMenu()" aria-label="Menu">
  <span></span><span></span><span></span>
</button>
<div class="mobile-menu" id="mobileMenu">
  <button class="close-btn" onclick="toggleMenu()">X</button>
  <a href="index.html">Accueil</a>
  <a href="jeux.html">Jeux</a>
  <a href="outils-gratuits.html">Outils gratuits</a>
  <a href="comparateurs.html">Comparateurs</a>
  <a href="a-propos.html">A propos</a>
  <a href="recherche.html">Rechercher</a>
</div>
<script>
function toggleMenu(){
  var m = document.getElementById("mobileMenu");
  m.classList.toggle("open");
  document.body.style.overflow = m.classList.contains("open") ? "hidden" : "";
}
</script>"""

count = 0
for f in os.listdir('.'):
    if f.endswith('.html') and f != 'index.html':
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        if 'hamburger' not in content:
            content = content.replace('</style>', hamburger_css + '\n</style>', 1)
            content = content.replace('</nav>', hamburger_html + '\n</nav>', 1)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            count += 1

print(str(count) + ' fichiers corrigés')