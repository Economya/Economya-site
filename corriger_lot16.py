#!/usr/bin/env python3
"""
Corrige 2 problemes trouves lors de l'audit qualite (lot 16) :

1. article-229.html (Reconversion professionnelle) : "en 2025" residuel
   dans le corps du texte alors que l'article est verifie juin 2026.

2. article-413.html (Arnaques en ligne) : URL cassee "plaine-en-ligne.masse.fr"
   -> le vrai site officiel est plainte-en-ligne.masecurite.interieur.gouv.fr

Idempotent. Sauvegardes .bak_lot16 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-229.html": [
        (
            "Les secteurs qui recrutent et paient bien en 2025",
            "Les secteurs qui recrutent et paient bien en 2026",
        ),
    ],
    "article-413.html": [
        (
            "plaine-en-ligne.masse.fr",
            "plainte-en-ligne.masecurite.interieur.gouv.fr",
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

    shutil.copy2(fichier, fichier + ".bak_lot16")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
