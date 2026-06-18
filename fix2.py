import os

count = 0
button = '<button class="hamburger" onclick="toggleMenu()" aria-label="Menu"><span></span><span></span><span></span></button><div class="mobile-menu" id="mobileMenu"><button class="close-btn" onclick="toggleMenu()">X</button><a href="index.html">Accueil</a><a href="jeux.html">Jeux</a><a href="outils-gratuits.html">Outils gratuits</a><a href="comparateurs.html">Comparateurs</a><a href="a-propos.html">A propos</a><a href="recherche.html">Rechercher</a></div>'

for f in os.listdir('.'):
    if not f.endswith('.html') or f == 'index.html':
        continue
    content = open(f, 'r', encoding='utf-8', errors='ignore').read()
    if 'button class="hamburger"' not in content:
        content = content.replace('</nav>', button + '</nav>', 1)
        open(f, 'w', encoding='utf-8').write(content)
        count += 1

print(str(count) + ' fichiers corriges')