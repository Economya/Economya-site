#!/usr/bin/env python3
"""
Corrige 2 problemes trouves lors de l'audit qualite (lot 15) :

1. article-438.html (Plus-value immobiliere) : taux global "36,2%"
   (19% IR + 17,2% PS) -> obsolete. Le taux PS 2026 confirme ailleurs
   sur le site est 18,6%, donc le taux global reel est 37,6%.

2. article-69.html (Aides primo-accedants) : "en 2025" residuel dans
   le corps du texte alors que l'article est verifie juin 2026.

Idempotent. Sauvegardes .bak_lot15 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-438.html": [
        (
            "vous pouvez être taxé jusqu'à 36,2 % (19 % d'IR + 17,2 % de prélèvements sociaux)",
            "vous pouvez être taxé jusqu'à 37,6 % (19 % d'IR + 18,6 % de prélèvements sociaux)",
        ),
        (
            "Prélèvements sociaux (17,2 %) 5 934 €",
            "Prélèvements sociaux (18,6 %) 6 409 €",
        ),
        (
            "Total taxe plus-value ≈ 11 882 €",
            "Total taxe plus-value ≈ 12 357 €",
        ),
    ],
    "article-69.html": [
        (
            "Voici les principaux dispositifs à connaître en 2025.",
            "Voici les principaux dispositifs à connaître en 2026.",
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

    shutil.copy2(fichier, fichier + ".bak_lot15")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
