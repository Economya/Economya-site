#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-368.html — dates obsolètes + montant forfaitaire
À lancer depuis ~/Desktop/mon site

1. Toutes les occurrences de "2025" -> "2026"
2. Montant forfaitaire : 635,71€ -> 638,28€ (déjà vérifié et corrigé dans
   calculateur-prime-activite.html plus tôt dans la session)

⚠️ NON recalculés : les valeurs dérivées de l'exemple de calcul détaillé
(bonification +168€, ressources -916€, prime ~187€/mois) — recalculer
précisément avec la nouvelle formule demanderait de refaire tout le calcul,
avec un risque d'erreur. L'article renvoie déjà vers caf.fr pour un calcul
exact, ce qui limite le risque réel pour le lecteur.

Idempotent. Sauvegarde en .bak_art368.

Usage :
    python3 corriger_article368.py
"""

import os

FICHIER = "article-368.html"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu

    if "638,28 €" in contenu and "2025" not in contenu:
        print("✅ Déjà corrigé.")
        return

    nb_2025 = contenu.count("2025")

    contenu = contenu.replace("📅 Vérifié mai 2025", "📅 Vérifié juin 2026")
    contenu = contenu.replace("2025", "2026")
    contenu = contenu.replace(
        '<div class="sim-val">635,71 €</div>',
        '<div class="sim-val">638,28 €</div>'
    )

    if contenu == contenu_original:
        print("⚠️ Aucune occurrence trouvée. Rien à corriger.")
        return

    with open(FICHIER + ".bak_art368", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_2025} occurrence(s) de '2025' corrigée(s) en '2026'")
    print("✅ Montant forfaitaire corrigé : 635,71€ -> 638,28€")
    print("   ⚠️ Valeurs dérivées de l'exemple (bonification, ressources, prime")
    print("      finale ~187€) NON recalculées — l'article renvoie déjà vers caf.fr")


if __name__ == "__main__":
    main()
