import os
import re

dossier = os.path.dirname(os.path.abspath(__file__))

# Etape 1 : extraire les vrais titres
print("Extraction des titres...")
titres = {}

for nom in os.listdir(dossier):
    m = re.match(r'article-(\d+)\.html', nom)
    if not m:
        continue
    num = int(m.group(1))
    chemin = os.path.join(dossier, nom)
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', contenu, re.DOTALL)
    if m_h1:
        titre = re.sub(r'<[^>]+>', '', m_h1.group(1)).strip()
        titre = titre.replace('\n', ' ').replace('  ', ' ').strip()
        titres[num] = titre
    else:
        m_title = re.search(r'<title>([^<]+)</title>', contenu)
        if m_title:
            titre = m_title.group(1).replace(' - Economya.fr', '').replace(' — Economya.fr', '').strip()
            titres[num] = titre

print(f"✅ {len(titres)} titres extraits")

# Etape 2 : corriger les titres dans les articles similaires
print("Correction des titres...")
corriges = 0

for nom in os.listdir(dossier):
    if not re.match(r'article-\d+\.html', nom):
        continue
    chemin = os.path.join(dossier, nom)
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if 'sim-card' not in contenu:
        continue
    nouveau = contenu
    
    # Remplacer Article NNN par vrai titre
    def remplacer(match):
        num = int(match.group(1))
        titre = titres.get(num, 'Article ' + str(num))
        if len(titre) > 60:
            titre = titre[:57] + '...'
        return '<div class="sim-card-title">' + titre + '</div>'
    
    nouveau = re.sub(r'<div class="sim-card-title">Article (\d+)</div>', remplacer, nouveau)
    
    # Corriger liens sans .html
    nouveau = re.sub(r'href="(article-\d+)">', r'href="\1.html">', nouveau)
    
    if nouveau != contenu:
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(nouveau)
        corriges += 1

print(f"✅ {corriges} articles corrigés")
input("\nAppuyez sur Entrée pour fermer...")
