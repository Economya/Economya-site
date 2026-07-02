#!/usr/bin/env python3
"""
Corrige 2 derniers residus du taux de prelevements sociaux obsolete
(17,2% -> 18,6%, deja corrige a de nombreux endroits cette session) :

1. article-338.html (Ouvrir son premier PEA)
2. article-342.html (Investir 100e/mois en Bourse)

Idempotent. Sauvegardes .bak_restants2 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-338.html": [
        (
            "0 % d'impôt sur les plus-values après 5 ans (hors prélèvements sociaux à 17,2 %)",
            "0 % d'impôt sur les plus-values après 5 ans (hors prélèvements sociaux à 18,6 %)",
        ),
    ],
    "article-342.html": [
        (
            "Après fiscalité PEA (17,2 % sur plus-values), les montants réels seront légèrement inférieurs.",
            "Après fiscalité PEA (18,6 % sur plus-values), les montants réels seront légèrement inférieurs.",
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

    shutil.copy2(fichier, fichier + ".bak_restants2")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
