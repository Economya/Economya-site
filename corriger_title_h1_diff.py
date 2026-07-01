#!/usr/bin/env python3
"""
Corrige les cas de VRAIE différence de texte entre <title> et <h1> repérés
lors du scan title-vs-h1 (ceux que corriger_h1_espaces.py a volontairement
ignorés car ce n'était pas qu'un problème d'espaces).

1. article-2.html : title dit "2025", h1 dit "2026" -> on aligne le title
   sur 2026 (le h1 est la source la plus fiable ici, cohérente avec le
   reste du site en 2026).

2. article-214.html : title et h1 racontent des choses différentes
   ("Colocation : bail, fiscalité, droits" vs "Bail en colocation :
   rédiger un contrat solide soi-même") -> on aligne le title sur le h1
   qui est plus descriptif et probablement le contenu réel de l'article.

3. article-500.html : structure différente entre title et h1 -> on aligne
   le h1 sur la structure du title (avec deux-points) pour cohérence SEO.

Idempotent. Sauvegarde .bak_titleh1_diff avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-2.html": [
        (
            "<title>Quel fournisseur d'électricité choisir en 2025 ? — Economya.fr</title>",
            "<title>Quel fournisseur d'électricité choisir en 2026 ? — Economya.fr</title>",
        ),
    ],
    "article-214.html": [
        (
            "<title>Colocation : bail, fiscalité, droits — Economya.fr</title>",
            "<title>Bail en colocation : rédiger un contrat solide soi-même — Economya.fr</title>",
        ),
    ],
    "article-500.html": [
        (
            "<title>500 articles : ce qu'on a vraiment appris sur l'argent — Economya.fr</title>",
            "<title>500 articles sur l'argent : ce qu'on a vraiment appris — Economya.fr</title>",
        ),
        (
            "<h1>500 articles sur l'argent\n      <em>ce qu'on a vraiment appris</em>\n    </h1>",
            "<h1>500 articles sur l'argent :\n      <em>ce qu'on a vraiment appris</em>\n    </h1>",
        ),
    ],
}


def corriger_fichier(fichier, remplacements):
    if not os.path.exists(fichier):
        print(f"  Fichier introuvable : {fichier} (ignore)")
        return

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in remplacements:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            print(f"  OK Corrige : {ancien[:55]}...")
            total += 1
        elif nouveau in contenu_modifie:
            print(f"  INFO Deja corrige (idempotent) : {nouveau[:55]}...")
        else:
            print(f"  ATTENTION chaine non trouvee : {ancien[:55]}...")

    if total == 0:
        print(f"  -> Rien a faire pour {fichier}.")
        return

    shutil.copy2(fichier, fichier + ".bak_titleh1_diff")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
