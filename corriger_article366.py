#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-366.html — dates obsolètes (2025 -> 2026)
À lancer depuis ~/Desktop/mon site

Cet article utilise des fourchettes de montants ("50 à 400€", "~200-400€"),
pas des taux légaux précis comme le RSA — les montants ne sont donc pas
modifiés, seulement les dates (2025 -> 2026), incluant le badge de
fraîcheur "Vérifié mai 2025" devenu trompeur (obsolète de plus d'un an).

Idempotent. Sauvegarde en .bak_art366.

Usage :
    python3 corriger_article366.py
"""

import os
import re

FICHIER = "article-366.html"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu

    if "Vérifié juin 2026" in contenu and "2025" not in contenu:
        print("✅ Déjà corrigé.")
        return

    nb_2025 = contenu.count("2025")

    # Cas spécial : badge de fraîcheur (avant le remplacement générique)
    contenu = contenu.replace("📅 Vérifié mai 2025", "📅 Vérifié juin 2026")

    # Remplacement générique de toutes les occurrences restantes de "2025"
    contenu = contenu.replace("2025", "2026")

    if contenu == contenu_original:
        print("⚠️ Aucune occurrence de '2025' trouvée. Rien à corriger.")
        return

    with open(FICHIER + ".bak_art366", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_2025} occurrence(s) de '2025' corrigée(s) en '2026' sur {FICHIER}")
    print("   (dont le badge 'Vérifié mai 2025' -> 'Vérifié juin 2026')")


if __name__ == "__main__":
    main()
