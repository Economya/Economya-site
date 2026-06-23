#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-261.html — bonus écologique obsolète + prime à la conversion supprimée
À lancer depuis ~/Desktop/mon site

1. Montant bonus écologique : 4 000€ -> 5 700€ (montant max 2026, ménages précaires,
   source officielle economie.gouv.fr, mise à jour 26/12/2025)
2. Intro : "2025" -> "2026", "jusqu'à 7 000€" -> "jusqu'à 7 700€"
3. Carte "Prime à la conversion" entièrement retirée — ce dispositif a été supprimé
   fin 2024, le présenter comme actif et cumulable est une erreur factuelle
4. Mention "Cumulable avec le bonus écologique" (à propos de la prime conversion,
   dans la carte vélo cargo électrique) -> retirée car elle référence un dispositif
   qui n'existe plus dans ce contexte précis -- en réalité cette phrase est sur la
   carte "vélo cargo", on la laisse, c'est correcte (parle d'aides régionales)

Idempotent. Sauvegarde en .bak_art261.

Usage :
    python3 corriger_article261.py
"""

import os
import re

FICHIER = "article-261.html"

ANCIENNE_INTRO = "Acheter un véhicule électrique en 2025 peut rapporter jusqu'à 7 000 € d'aides cumulées entre le bonus écologique et la prime à la conversion. Des conditions de revenus et de résidence s'appliquent. Voici le guide complet pour ne rien rater."
NOUVELLE_INTRO = "Acheter un véhicule électrique en 2026 peut rapporter jusqu'à 7 700 € d'aides cumulées grâce au bonus écologique et au surbonus batterie européenne. Des conditions de revenus et de résidence s'appliquent. Voici le guide complet pour ne rien rater."

ANCIEN_MONTANT_BONUS = '''<div class="bcard-name">Bonus écologique voiture électrique</div>
      <div class="bcard-amount">4 000 €</div>'''
NOUVEAU_MONTANT_BONUS = '''<div class="bcard-name">Bonus écologique voiture électrique</div>
      <div class="bcard-amount">Jusqu'à 5 700 €</div>'''

# Carte "Prime à la conversion" entière à retirer (dispositif supprimé fin 2024)
PATTERN_CARTE_CONVERSION = re.compile(
    r'\s*<div class="bcard">\s*<div class="bcard-icon">🔄</div>\s*'
    r'<div class="bcard-name">Prime à la conversion</div>\s*'
    r'<div class="bcard-amount">1 500 €</div>\s*'
    r'<div class="bcard-cond">.*?</div>\s*'
    r'</div>',
    re.DOTALL
)


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    modifications = []

    if ANCIENNE_INTRO in contenu:
        contenu = contenu.replace(ANCIENNE_INTRO, NOUVELLE_INTRO, 1)
        modifications.append("Intro mise à jour (2026, 7 700€)")

    if ANCIEN_MONTANT_BONUS in contenu:
        contenu = contenu.replace(ANCIEN_MONTANT_BONUS, NOUVEAU_MONTANT_BONUS, 1)
        modifications.append("Montant bonus écologique corrigé (5 700€)")

    if PATTERN_CARTE_CONVERSION.search(contenu):
        contenu = PATTERN_CARTE_CONVERSION.sub('', contenu, count=1)
        modifications.append("Carte 'Prime à la conversion' retirée (dispositif supprimé)")

    if not modifications:
        print("✅ Déjà corrigé ou texte attendu non trouvé.")
        return

    with open(FICHIER + ".bak_art261", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print("✅ Corrections appliquées :")
    for m in modifications:
        print(f"   - {m}")


if __name__ == "__main__":
    main()
