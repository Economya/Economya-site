#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-43.html — combles perdus exclus + mécanisme PAC corrigé
À lancer depuis ~/Desktop/mon site

1. "Isolation des combles perdus... MaPrimeRénov' jusqu'à 75%" : les
   combles perdus sont exclus du parcours par geste depuis le 1er janvier
   2026 (nécessitent une rénovation d'ampleur). Le forfait 75€/m² reste
   valable uniquement pour les rampants/combles aménagés.
2. "Pompe à chaleur... MaPrimeRénov' jusqu'à 70%" : erreur de mécanisme —
   l'aide PAC air/eau est un FORFAIT FIXE (5 000/4 000/3 000€ selon
   revenus, vérifié sur d'autres articles), pas un pourcentage du coût.

Idempotent. Sauvegarde en .bak_art43.

Usage :
    python3 corriger_article43.py
"""

import os

FICHIER = "article-43.html"

REMPLACEMENTS = [
    (
        '<div class="travaux-name">Isolation des combles</div>\n      <div class="travaux-desc">30% des déperditions thermiques passent par le toit. Isolation des combles perdus : 15 à 25€/m². Soufflage en 1 journée.</div>\n      <div class="travaux-aide">MaPrimeRénov\' jusqu\'à 75%</div>',
        '<div class="travaux-name">Isolation des combles</div>\n      <div class="travaux-desc">30% des déperditions thermiques passent par le toit. Isolation des combles perdus : 15 à 25€/m². Soufflage en 1 journée. ⚠️ Depuis 2026, les combles perdus ne sont plus éligibles au parcours simple MaPrimeRénov\' (réservé désormais aux rampants/combles aménagés, jusqu\'à 75€/m²) — ils nécessitent une rénovation d\'ampleur.</div>\n      <div class="travaux-aide">Variable selon parcours</div>',
    ),
    (
        '<div class="travaux-name">Pompe à chaleur</div>\n      <div class="travaux-desc">Remplace une chaudière gaz par un système 3x plus efficace. Investissement 8 000-15 000€, mais aides très importantes.</div>\n      <div class="travaux-aide">MaPrimeRénov\' jusqu\'à 70%</div>',
        '<div class="travaux-name">Pompe à chaleur</div>\n      <div class="travaux-desc">Remplace une chaudière gaz par un système 3x plus efficace. Investissement 8 000-15 000€, mais aides très importantes.</div>\n      <div class="travaux-aide">MaPrimeRénov\' jusqu\'à 5 000€ (forfait selon revenus)</div>',
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

    with open(FICHIER + ".bak_art43", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Combles perdus exclus 2026, PAC corrige en forfait (5000e max)")


if __name__ == "__main__":
    main()
