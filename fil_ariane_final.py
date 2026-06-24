#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final fil d'Ariane — corrige le bug CSS ET ajoute les catégories
manquantes pour les fichiers utilisant la classe "article-cat" (variante
non détectée par le premier script, qui ne cherchait que "cat-pill")
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Pour CHAQUE fichier article-*.html ayant déjà un fil d'Ariane :
1. Si le fichier a une catégorie via "article-cat" (ex: 💳 Banque) ET que
   le fil d'Ariane actuel ne l'a PAS (juste Accueil > Titre) : reconstruit
   le fil d'Ariane en 3 niveaux avec la vraie catégorie.
2. Corrige systématiquement le bug CSS (<nav> -> <div>) qui causait
   l'étalement visuel bizarre, qu'il y ait une catégorie ou non.

Idempotent. Sauvegarde en .bak_finalbreadcrumb avant modification.

Usage :
    python3 fil_ariane_final.py
"""

import os
import re
import glob
import json

PATTERN_BREADCRUMB_NAV = re.compile(
    r"<nav aria-label=\"Fil d'Ariane\" style=\"([^\"]*)\">\s*(.*?)\s*</nav>\s*<script type=\"application/ld\+json\">(.*?)</script>",
    re.DOTALL
)
PATTERN_ARTICLE_CAT = re.compile(r'<div class="article-cat">([^<]*)</div>')
PATTERN_CATPILL = re.compile(r'<div class="cat-pill">([^<]*)</div>')


def nettoyer_categorie(cat_brute):
    texte = re.sub(r'^[^\wÀ-ÿ]+', '', cat_brute).strip()
    return texte


def construire_breadcrumb_complet(categorie, titre, url_fichier):
    titre_court = titre if len(titre) <= 60 else titre[:57] + "..."
    style = "max-width:900px;margin:0 auto;padding:.7rem 1.5rem;font-size:.78rem;color:var(--m,#5F5E5A);display:flex;flex-wrap:wrap;align-items:center;gap:.35rem"

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

    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items_schema}
    return (
        f'<div role="navigation" aria-label="Fil d\'Ariane" style="{style}">{fil_visuel}</div>\n'
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
    )


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "role=\"navigation\" aria-label=\"Fil d'Ariane\"" in contenu:
        return "déjà corrigé (v2)"

    match_breadcrumb = PATTERN_BREADCRUMB_NAV.search(contenu)
    if not match_breadcrumb:
        return "pas de fil d'Ariane v1 trouvé"

    titre_actuel = match_breadcrumb.group(2)
    m_titre = re.search(r'<span[^>]*>([^<]+)</span>\s*$', titre_actuel)
    titre = m_titre.group(1).strip() if m_titre else "Article"

    match_articlecat = PATTERN_ARTICLE_CAT.search(contenu)
    match_catpill = PATTERN_CATPILL.search(contenu)

    if match_articlecat:
        categorie = nettoyer_categorie(match_articlecat.group(1))
    elif match_catpill:
        categorie = nettoyer_categorie(match_catpill.group(1))
    else:
        categorie = None

    nouveau_breadcrumb = construire_breadcrumb_complet(categorie, titre, os.path.basename(chemin))

    nouveau_contenu = contenu[:match_breadcrumb.start()] + nouveau_breadcrumb + contenu[match_breadcrumb.end():]

    with open(chemin + ".bak_finalbreadcrumb", 'w', encoding='utf-8') as f:
        f.write(contenu)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return f"corrigé (catégorie: {categorie or 'aucune'})"


def main():
    fichiers = sorted(glob.glob("article-*.html")) + sorted(glob.glob("calculateur-*.html")) + sorted(glob.glob("simulateur-*.html")) + sorted(glob.glob("comparateur-*.html"))
    fichiers = sorted(set(fichiers))
    resultats = {}

    for fichier in fichiers:
        statut = traiter_fichier(fichier)
        cle = statut.split(" (")[0] if "corrigé (catégorie" in statut else statut
        resultats[cle] = resultats.get(cle, 0) + 1

    print("=== RÉSUMÉ ===")
    for statut, count in resultats.items():
        print(f"{statut} : {count}")


if __name__ == "__main__":
    main()
