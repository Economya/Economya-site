import os
import re

dossier = os.path.dirname(os.path.abspath(__file__))

# Thématiques par numéros d'articles
THEMES = {
    "Immobilier": list(range(201, 216)),
    "Emploi": list(range(216, 231)),
    "Sante": list(range(231, 246)),
    "Tech": list(range(246, 261)),
    "Transport": list(range(261, 276)),
    "Voyages": list(range(276, 291)) + list(range(478, 481)),
    "Alimentation": list(range(291, 306)),
    "Famille": list(range(306, 321)),
    "Ecologie": list(range(321, 336)),
    "Investissement": list(range(336, 351)) + [453, 473, 474, 496],
    "Formation": list(range(351, 366)),
    "Social": list(range(366, 374)),
    "Finance": list(range(374, 415)) + list(range(430, 445)) + list(range(481, 500)),
    "Revenus": list(range(415, 430)) + list(range(442, 444)) + list(range(467, 470)) + list(range(483, 485)),
    "Lifestyle": list(range(387, 402)) + list(range(454, 466)) + list(range(471, 478)),
}

# Titres des articles (extrait depuis index)
TITRES = {
    201: "Acheter sa résidence principale : le guide 2025",
    202: "Renégocier son crédit immobilier",
    203: "PTZ 2025 : conditions et simulation",
    204: "Frais de notaire : comment les calculer",
    205: "Dépôt de garantie : récupérer sa caution",
    206: "Rénovation énergétique : toutes les aides 2025",
    207: "Investir en LMNP : guide complet",
    208: "Charges de copropriété : comment les contester",
    209: "Home staging : valoriser son bien pour vendre",
    210: "Bail locatif : droits et obligations",
    216: "Bulletin de salaire : décrypter chaque ligne",
    217: "Négocier son salaire : scripts qui marchent",
    218: "Chômage ARE : calculer ses droits en 2025",
    219: "Rupture conventionnelle : tout savoir",
    220: "Démissionner pour reconversion : droits au chômage",
    336: "ETF World : comment investir simplement",
    337: "Livret A vs LEP vs LDDS : que choisir",
    338: "Ouvrir son premier PEA",
    339: "PEA : ouvrir, gérer, optimiser",
    340: "Fonds euros vs unités de compte",
    374: "Budget zéro basé : méthode et application",
    375: "Méthode 50/30/20 : appliquer concrètement",
    376: "YNAB vs Bankin vs Linxo",
    447: "Matelas de sécurité : calculer en 6 mois",
    448: "Urgences financières : le plan de survie",
    495: "Taux d'épargne de 50% : comment y arriver",
    496: "Actions françaises à dividende : sélection 2025",
    497: "Défiscalisation : toutes les niches légales 2025",
    483: "Micro-BIC vs BNC : quel régime choisir",
    484: "ACRE : exonération de cotisations",
    485: "Médiation bancaire : quand y recourir",
    486: "Négociation avec les créanciers",
    487: "Microcrédit : accéder au financement sans banque",
    488: "Droit à l'oubli bancaire",
    489: "BPI France : aides aux entrepreneurs",
    490: "Aides régionales : trouver celles disponibles",
    491: "Carte Mastercard World Elite gratuite",
    492: "Revolut, N26, Lydia : quelle néobanque",
    493: "Caisse des Dépôts : avoirs oubliés",
    494: "Work and travel : travailler en voyageant",
    499: "L'avenir de l'économie frugale",
    500: "500 articles : ce qu'on a appris sur l'argent",
}

def get_theme(num):
    for theme, nums in THEMES.items():
        if num in nums:
            return theme
    return None

def get_similaires(num, max=4):
    theme = get_theme(num)
    if not theme:
        return []
    similaires = []
    for n in THEMES.get(theme, []):
        if n != num and n != num-1 and n != num+1:
            similaires.append(n)
        if len(similaires) >= max:
            break
    return similaires[:max]

# CSS pour la section
CSS_SIMILAIRES = """
<style>
.similaires{max-width:760px;margin:2rem auto;padding:0 2rem 1rem}
.similaires h3{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;margin-bottom:1rem;color:#085041}
.sim-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.8rem}
.sim-card{background:#fff;border:1px solid rgba(0,0,0,0.08);border-radius:12px;padding:.9rem;text-decoration:none;color:#2C2C2A;transition:transform .2s,box-shadow .2s;display:block}
.sim-card:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(29,158,117,.1)}
.sim-card-title{font-size:.82rem;font-weight:600;line-height:1.3;color:#085041}
.sim-card-cat{font-size:.68rem;color:#1D9E75;font-weight:500;margin-bottom:.3rem;text-transform:uppercase}
</style>
"""

fichiers = [f for f in os.listdir(dossier) if re.match(r'article-\d+\.html', f)]
modifies = 0
deja = 0

for nom in fichiers:
    m = re.search(r'article-(\d+)\.html', nom)
    if not m:
        continue
    num = int(m.group(1))
    chemin = os.path.join(dossier, nom)
    
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    if 'similaires' in contenu:
        deja += 1
        continue
    
    similaires = get_similaires(num)
    if not similaires:
        continue
    
    theme = get_theme(num)
    
    # Construire la section HTML
    cards = ""
    for s in similaires:
        titre = TITRES.get(s, f'Article {s}')
        cards += f'''<a class="sim-card" href="article-{s}.html"><div class="sim-card-cat">{theme}</div><div class="sim-card-title">{titre}</div></a>'''
    
    section = f'''{CSS_SIMILAIRES}
<div class="similaires">
  <h3>📚 Articles similaires</h3>
  <div class="sim-grid">{cards}</div>
</div>'''
    
    nouveau = contenu.replace('</body>', section + '\n</body>', 1)
    
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    modifies += 1

print(f"✅ {modifies} articles mis à jour avec la section Articles similaires")
print(f"ℹ️  {deja} articles avaient déjà la section")
input("\nAppuyez sur Entrée pour fermer...")
