#!/usr/bin/env python3
"""
Corrige les 5 problèmes trouvés lors de l'audit de comparateurs.html :

1. article-337.html : "LEP en priorité (4 %)" -> "LEP en priorité (2,5 %)"
2. article-337.html : fil d'Ariane + JSON-LD "que choisir en 2025" -> "2026" (x2)
3. article-249.html : badge "5G dès 6 €/mois" -> "5G dès 6,99 €/mois" (x5)
4. comparateurs.html : "Dès 6 €/mois" -> "Dès 6,99 €/mois" (carte Forfaits 5G)
5. comparateurs.html : tag "Avast" -> "DaVinci Resolve" (carte Logiciels gratuits,
   Avast n'est mentionné nulle part dans article-141.html)
6. simulateur-credit-immo.html : taux par défaut 3,5% -> 3,4%

Idempotent : relancer ce script sans rien à corriger ne fait rien.
Sauvegarde .bak_auditcomparateurs avant chaque modification.
"""

import os
import shutil

# (fichier, [(ancien, nouveau, occurrences_attendues), ...])
CORRECTIONS = {
    "article-337.html": [
        (
            "LEP en priorité (4 %), puis Livret A + LDDS",
            "LEP en priorité (2,5 %), puis Livret A + LDDS",
            1,
        ),
        (
            "Livret A vs LEP vs LDDS : que choisir en 2025",
            "Livret A vs LEP vs LDDS : que choisir en 2026",
            2,
        ),
    ],
    "article-249.html": [
        (
            "5G dès 6 €/mois",
            "5G dès 6,99 €/mois",
            5,
        ),
    ],
    "comparateurs.html": [
        (
            "Dès 6 €/mois",
            "Dès 6,99 €/mois",
            1,
        ),
        (
            '<span class="comp-item">Avast</span>',
            '<span class="comp-item">DaVinci Resolve</span>',
            1,
        ),
    ],
    "simulateur-credit-immo.html": [
        (
            'value="3.5"',
            'value="3.4"',
            1,
        ),
        (
            '3,5 <span>%</span>',
            '3,4 <span>%</span>',
            1,
        ),
    ],
}


def corriger_fichier(fichier, remplacements):
    if not os.path.exists(fichier):
        print(f"❌ Fichier introuvable : {fichier} (ignoré)")
        return

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total_corrections = 0

    for ancien, nouveau, _attendu in remplacements:
        nb_avant = contenu_modifie.count(ancien)
        if nb_avant > 0:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau)
            print(f"  ✅ {fichier} : {nb_avant} occurrence(s) de '{ancien[:45]}...' corrigée(s)")
            total_corrections += nb_avant
        elif nouveau in contenu_modifie:
            print(f"  ℹ️  {fichier} : déjà corrigé (idempotent) '{nouveau[:45]}...'")
        else:
            print(f"  ⚠️  {fichier} : chaîne non trouvée '{ancien[:45]}...'")

    if total_corrections == 0:
        print(f"  → Rien à faire pour {fichier}.")
        return

    shutil.copy2(fichier, fichier + ".bak_auditcomparateurs")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  → {total_corrections} correction(s) écrite(s) dans {fichier} (sauvegarde créée)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
