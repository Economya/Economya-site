#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction de l'ordre structurel : "Articles similaires" doit venir AVANT
le <footer>, pas après (bug visuel : le footer apparaît au milieu de la
page au lieu d'être le dernier élément)
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Repère le bloc <footer>...</footer> suivi du bloc <style>.similaires...
</style><div class="similaires">...</div>, et inverse leur ordre.

Idempotent. Sauvegarde en .bak_footerorder avant modification.

Usage :
    python3 corriger_ordre_footer.py
"""

import os
import re
import glob

PATTERN = re.compile(
    r'(<footer>.*?</footer>)\s*'
    r'(<style>\s*\.similaires.*?)(?=<script>function toggleMenu)',
    re.DOTALL
)


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    match = PATTERN.search(contenu)
    if not match:
        return "motif non trouvé"

    bloc_footer = match.group(1)
    bloc_similaires = match.group(2)

    # Si déjà dans le bon ordre (similaires avant footer), ne rien faire
    # (le pattern ne matcherait pas dans ce cas précis, donc cette vérif
    # est surtout une sécurité supplémentaire)

    nouveau_bloc = bloc_similaires + "\n\n" + bloc_footer

    nouveau_contenu = contenu[:match.start()] + nouveau_bloc + contenu[match.end():]

    with open(chemin + ".bak_footerorder", 'w', encoding='utf-8') as f:
        f.write(contenu)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return "corrigé"


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
