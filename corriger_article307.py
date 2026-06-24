#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-307.html — prime naissance et plafond IJ maternité obsolètes
À lancer depuis ~/Desktop/mon site

Corrections vérifiées (revalorisation 1er avril 2026, sources convergentes) :
1. Prime de naissance : badge "Jusqu'à 1 000€" -> "Jusqu'à 1 093€" (montant réel
   plus élevé que ce qui était annoncé, sous-estimation à corriger)
2. "Vérifié mai 2025" -> "Vérifié juin 2026" (badge fraîcheur obsolète)
3. Plafond IJ congé maternité : 91,96€/jour (2025) -> 104,02€/jour (2026)

Idempotent. Sauvegarde en .bak_art307.

Usage :
    python3 corriger_article307.py
"""

import os

FICHIER = "article-307.html"

REMPLACEMENTS = [
    (
        "Prime naissance CAF : toutes les aides — Jusqu'à 1 000€ à la naissance. Guide complet sur Economya.fr",
        "Prime naissance CAF : toutes les aides — Jusqu'à 1 093€ à la naissance. Guide complet sur Economya.fr",
    ),
    (
        "💰 Jusqu'à 1 000 € à la naissance",
        "💰 Jusqu'à 1 093 € à la naissance",
    ),
    (
        "📅 Vérifié mai 2025",
        "📅 Vérifié juin 2026",
    ),
    (
        "Aide unique versée avant la naissance pour préparer l'arrivée du bébé. Montant 2025 selon revenus du foyer. Sous conditions de ressources.",
        "Aide unique versée avant la naissance pour préparer l'arrivée du bébé. Montant 2026 selon revenus du foyer. Sous conditions de ressources.",
    ),
    (
        "L'assurance maladie verse des indemnités journalières égales à 100 % du salaire net dans la limite du plafond Sécu (~91,96 €/jour en 2025).",
        "L'assurance maladie verse des indemnités journalières égales à 100 % du salaire net dans la limite du plafond Sécu (~104,02 €/jour en 2026).",
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    for ancien, nouveau in REMPLACEMENTS:
        if nouveau in contenu and ancien not in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art307", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")


if __name__ == "__main__":
    main()
