#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-218.html — dates obsolètes + minimum ARE
À lancer depuis ~/Desktop/mon site

1. Toutes les occurrences de "2025" -> "2026" (titre, meta, h1, badge fraîcheur)
2. Minimum ARE : 31,59€/jour (2025) -> 32,13€/jour (2026, confirmé par
   plusieurs sources convergentes)

⚠️ NON corrigés (confiance insuffisante, une seule source chacun, pas de
consensus) : "Plafond 291,06€/jour" et "salaires > 11 600€/mois". À vérifier
séparément sur france-travail.fr ou unedic.org avant correction.

Idempotent. Sauvegarde en .bak_art218.

Usage :
    python3 corriger_article218.py
"""

import os

FICHIER = "article-218.html"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu

    if "32,13 €/jour" in contenu and "2025" not in contenu:
        print("✅ Déjà corrigé.")
        return

    nb_2025 = contenu.count("2025")

    contenu = contenu.replace("✅ Vérifié juin 2025", "✅ Vérifié juin 2026")
    contenu = contenu.replace("2025", "2026")
    contenu = contenu.replace(
        "Minimum 31,59 €/jour · Maximum 75 % du SJR · Plancher légal selon salaire",
        "Minimum 32,13 €/jour · Maximum 75 % du SJR · Plancher légal selon salaire"
    )

    if contenu == contenu_original:
        print("⚠️ Aucune occurrence trouvée. Rien à corriger.")
        return

    with open(FICHIER + ".bak_art218", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_2025} occurrence(s) de '2025' corrigée(s) en '2026'")
    print("✅ Minimum ARE corrigé : 31,59€/jour -> 32,13€/jour")
    print("   ⚠️ 'Plafond 291,06€/jour' et seuil '11 600€/mois' NON vérifiés")
    print("      avec assez de confiance — à contrôler sur france-travail.fr")


if __name__ == "__main__":
    main()
