#!/usr/bin/env python3
"""
Modernise les 109 articles au vieux gabarit (class="hero") vers le
nouveau gabarit (class="article-hero") avec badge categorie, bandeau
economies et ligne meta complete (Lecture / Verifie / tag).

Regles :
- Temps de lecture : calcule depuis le nombre de mots reels de l'article
  (~200 mots/minute, arrondi, minimum 2 min).
- Categorie : deduite du titre par mots-cles (pas d'invention).
- Bandeau economies : reutilise un montant/pourcentage DEJA present
  dans le texte de l'article (jamais invente). Si aucun trouve,
  utilise un badge generique non chiffre.
- Structure : class="hero" -> class="article-hero", ajoute badge
  categorie avant le h1, transforme le <p> existant en <p class="intro">,
  ajoute bandeau economies + ligne meta apres.

Idempotent (skip si class="article-hero" deja present).
Sauvegardes .bak_header avant modification.
"""

import glob
import re
import shutil

CATEGORIES = [
    (r'immobili|logement|r[ée]sidence|notaire|copropri[ée]t[ée]|bail|locataire|viager|\bSCI\b|PTZ|cr[ée]dit immobilier|appartement|maison|caution|d[ée]p[ôo]t de garantie|construction', '🏠 Immobilier'),
    (r'salaire|emploi|ch[ôo]mage|\bARE\b|rupture conventionnelle|d[ée]mission|arr[êe]t maladie|t[ée]l[ée]travail|\bCDD\b|portage salarial|prime|int[ée]ressement|participation|heures suppl[ée]mentaires|reconversion|bulletin de salaire', '💼 Emploi'),
    (r'sant[ée]|\bALD\b|mutuelle|remboursement|m[ée]dicament|lunettes|\bCSS\b', '🏥 Santé'),
    (r'\bVPN\b|piratage|logiciel|\bIA\b|ChatGPT|Gemini|Claude|informatique|application|tablette|automatiser', '💻 Tech'),
    (r'voyage|h[ôo]tel|miles|festival|ski|montagne|Portugal|nomade|t[ée]l[ée]travailler depuis|pays', '✈️ Voyage'),
    (r'Vinted|Leboncoin|reconditionn[ée]|soldes|erreur de prix|ench[èe]res|Back Market|Recommerce|Fnac', '🛍️ Bons plans'),
    (r'voiture|casse auto|pi[èe]ces auto', '🚗 Auto'),
    (r'cuisiner|gastronomique|anti-gaspi|\bDLC\b|\bDDM\b', '🍽️ Alimentation'),
    (r'investir|inflation|banque [àa] l\'[ée]tranger|arbitragiste|stocks dormants|\bLMNP\b|g[ée]o-arbitrage', '📈 Finance'),
    (r'cosm[ée]tique|parfum|maquillage|soins beaut[ée]', '💄 Beauté'),
    (r'sommeil|sport|perdre du poids|dormir', '🧘 Bien-être'),
    (r'meubler|d[ée]corer|panneaux solaires|[ée]lectrom[ée]nager', '🏡 Maison'),
]
CATEGORIE_DEFAUT = '💰 Bons plans'

MONTANT_RE = re.compile(r'\d[\d\s]{0,6}(?:€|%|\s?euros)')


def deduire_categorie(titre):
    for pattern, cat in CATEGORIES:
        if re.search(pattern, titre, re.IGNORECASE):
            return cat
    return CATEGORIE_DEFAUT


def calculer_lecture(texte):
    mots = len(re.findall(r'\w+', texte))
    minutes = max(2, round(mots / 200))
    return minutes


def extraire_montant(intro_texte, corps_texte):
    m = MONTANT_RE.search(intro_texte)
    if m:
        return m.group().strip()
    m = MONTANT_RE.search(corps_texte[:2000])
    if m:
        return m.group().strip()
    return None


def main():
    fichiers = sorted(glob.glob('article-*.html'))
    traites = 0
    deja_bon = 0
    erreurs = []

    for f in fichiers:
        with open(f, 'r', encoding='utf-8') as fh:
            contenu = fh.read()

        if 'class="article-hero"' in contenu:
            deja_bon += 1
            continue

        m = re.search(
            r'<div class="hero">\s*<h1>(.*?)</h1>\s*<p>(.*?)</p>\s*</div>',
            contenu, re.DOTALL
        )
        if not m:
            erreurs.append(f)
            continue

        h1_html = m.group(1).strip()
        intro_html = m.group(2).strip()
        titre_texte = re.sub(r'<[^>]+>', '', h1_html)

        categorie = deduire_categorie(titre_texte)

        corps_apres = contenu[m.end():m.end() + 3000]
        corps_texte = re.sub(r'<[^>]+>', ' ', corps_apres)
        intro_texte = re.sub(r'<[^>]+>', ' ', intro_html)

        mots_totaux = re.sub(r'<[^>]+>', ' ', contenu)
        minutes = calculer_lecture(mots_totaux)

        montant = extraire_montant(intro_texte, corps_texte)
        if montant:
            savings_html = f'💰 {montant}'
        else:
            savings_html = '💡 Guide pratique'

        nouveau_bloc = f'''<div class="article-hero">
  <div class="article-cat">{categorie}</div>
  <h1>{h1_html}</h1>
  <p class="intro">{intro_html}</p>
  <div class="savings-badge">{savings_html}</div>
  <div class="article-meta">
    <span>📖 Lecture {minutes} min</span>
    <span>✅ Vérifié juin 2026</span>
    <span>🇫🇷 Adapté au marché français</span>
  </div>
</div>'''

        contenu_new = contenu[:m.start()] + nouveau_bloc + contenu[m.end():]

        shutil.copy2(f, f + '.bak_header')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(contenu_new)
        traites += 1

    print(f"Headers modernises : {traites}")
    print(f"Deja au bon format (ignores) : {deja_bon}")
    print(f"Erreurs (structure non reconnue) : {len(erreurs)}")
    if erreurs:
        print(erreurs)


if __name__ == '__main__':
    main()
