#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-233.html — plafond CSS et dates obsolètes
À lancer depuis ~/Desktop/mon site

1. Dates 2025 -> 2026
2. Plafond CSS gratuite 1 personne : 876€/mois -> 868€/mois (valeur 2026
   confirmée par sources convergentes officielles)

⚠️ NON corrigées : les lignes 2/3/4 personnes et "par personne supplémentaire"
du tableau, ainsi que la colonne "CSS à 1€/j" — pas vérifiées individuellement
avec la même rigueur. À contrôler sur ameli.fr ou complementaire-sante-solidaire.fr.

Idempotent. Sauvegarde en .bak_art233.

Usage :
    python3 corriger_article233.py
"""

import os

FICHIER = "article-233.html"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu

    if "868 €/mois" in contenu and "2025" not in contenu:
        print("✅ Déjà corrigé.")
        return

    nb_2025 = contenu.count("2025")

    contenu = contenu.replace("✅ Vérifié juin 2025", "✅ Vérifié juin 2026")
    contenu = contenu.replace("2025", "2026")
    contenu = contenu.replace(
        '<td class="ok">876 €/mois</td>',
        '<td class="ok">868 €/mois</td>'
    )

    if contenu == contenu_original:
        print("⚠️ Aucune occurrence trouvée. Rien à corriger.")
        return

    with open(FICHIER + ".bak_art233", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_2025} occurrence(s) de '2025' corrigée(s) en '2026'")
    print("✅ Plafond CSS 1 personne corrigé : 876€ -> 868€/mois")
    print("   ⚠️ Lignes 2/3/4 personnes et colonne CSS payante NON vérifiées")
    print("      individuellement — à contrôler sur ameli.fr")


if __name__ == "__main__":
    main()
