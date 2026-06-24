#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajout d'un fil d'Ariane (breadcrumb) sur tous les articles
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Extrait la catégorie depuis le badge déjà présent sur chaque page
(<div class="cat-pill">EMOJI Catégorie</div>) et le titre depuis le <h1>,
puis insère :
1. Un fil d'Ariane visuel juste après le menu mobile
2. Un schema.org BreadcrumbList (JSON-LD) pour le SEO

Idempotent. Sauvegarde en .bak_breadcrumb avant modification.

Usage :
    python3 ajouter_fil_ariane.py
"""

import os
import re
import glob
import json

PATTERN_CATPILL = re.compile(r'<div class="cat-pill">([^<]*)</div>')
PATTERN_H1 = re.compile(r'<h1>(.*?)</h1>', re.DOTALL)
PATTERN_MOBILE_MENU_END = re.compile(r'(<div class="mobile-menu"[^>]*>.*?</div>)', re.DOTALL)


def nettoyer_titre(titre_html):
    # Retire les balises HTML internes (br, em, etc.) et les emojis de début
    texte = re.sub(r'<[^>]+>', ' ', titre_html)
    texte = re.sub(r'\s+', ' ', texte).strip()
    return texte


def nettoyer_categorie(cat_brute):
    # Retire l'emoji au début (garde uniquement lettres/espaces/apostrophes)
    texte = re.sub(r'^[^\wÀ-ÿ]+', '', cat_brute).strip()
    return texte


def construire_breadcrumb(categorie, titre, url_fichier):
    titre_court = titre if len(titre) <= 60 else titre[:57] + "..."

    if categorie:
        fil_visuel = f'<a href="index.html" style="color:inherit;text-decoration:none">Accueil</a> › <span>{categorie}</span> › <span style="color:var(--t,#2C2C2A)">{titre_court}</span>'
        items_schema = [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://economya.fr/index.html"},
            {"@type": "ListItem", "position": 2, "name": categorie, "item": "https://economya.fr/index.html"},
            {"@type": "ListItem", "position": 3, "name": titre_court, "item": f"https://economya.fr/{url_fichier}"},
        ]
    else:
        fil_visuel = f'<a href="index.html" style="color:inherit;text-decoration:none">Accueil</a> › <span style="color:var(--t,#2C2C2A)">{titre_court}</span>'
        items_schema = [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://economya.fr/index.html"},
            {"@type": "ListItem", "position": 2, "name": titre_court, "item": f"https://economya.fr/{url_fichier}"},
        ]

    html_visuel = f'''<nav aria-label="Fil d'Ariane" style="max-width:900px;margin:0 auto;padding:.7rem 1.5rem;font-size:.78rem;color:var(--m,#5F5E5A)">
  {fil_visuel}
</nav>'''

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items_schema
    }
    html_schema = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

    return html_visuel + "\n" + html_schema + "\n"


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "Fil d'Ariane" in contenu:
        return "déjà présent"

    match_cat = PATTERN_CATPILL.search(contenu)
    match_h1 = PATTERN_H1.search(contenu)

    if not match_h1:
        return "h1 non trouvé"

    categorie = nettoyer_categorie(match_cat.group(1)) if match_cat else None
    titre = nettoyer_titre(match_h1.group(1))

    match_menu = PATTERN_MOBILE_MENU_END.search(contenu)
    if not match_menu:
        return "menu mobile non trouvé"

    breadcrumb_html = construire_breadcrumb(categorie, titre, os.path.basename(chemin))

    position_insertion = match_menu.end()
    nouveau_contenu = (
        contenu[:position_insertion]
        + "\n" + breadcrumb_html
        + contenu[position_insertion:]
    )

    with open(chemin + ".bak_breadcrumb", 'w', encoding='utf-8') as f:
        f.write(contenu)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return "ajouté"


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    resultats = {}

    for fichier in fichiers:
        statut = traiter_fichier(fichier)
        resultats[statut] = resultats.get(statut, 0) + 1

    print("=== RÉSUMÉ ===")
    for statut, count in resultats.items():
        print(f"{statut} : {count}")


if __name__ == "__main__":
    main()
