#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du lot article-216/219/221/222/224 — plusieurs chiffres basés
sur le PASS obsolète + une réforme structurelle non reflétée (IJSS)
À lancer depuis ~/Desktop/mon site

Découvertes (sources officielles convergentes) :
- PASS 2026 confirmé : 48 060€ (vs 47 100€ en 2025, 46 368€ en 2024,
  43 992€ en 2023 — plusieurs articles utilisaient des PASS d'années
  différentes, jamais mis à jour)
- article-216 : titre-restaurant, plafond exonération 7,18€ -> 7,32€/titre
- article-219 : indemnité de rupture, 2×PASS = 92 736€ (PASS 2024) -> 96 120€
  (PASS 2026)
- article-221 : RÉFORME STRUCTURELLE non reflétée — depuis le 20/02/2025,
  le plafond de calcul des IJSS est passé de 1,8 à 1,4 SMIC. Montant
  actuel (depuis le 01/02/2026) : 41,95€/jour (53,49€ était l'ANCIEN
  calcul à 1,8 SMIC, periode pré-réforme)
- article-222 : date seulement (montant 2,70€/jour déjà confirmé correct)
- article-224 : 75% PASS = 32 994€ (PASS 2023) -> 36 045€ (PASS 2026) ;
  8% PASS = 3 519€ -> 3 845€ (même calcul déjà corrigé ailleurs aujourd'hui)

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot216_224.py
"""

import os

REMPLACEMENTS = {
    "article-216.html": [
        (
            "<span class=\"bull-montant gris\">Période : juin 2025</span>",
            "<span class=\"bull-montant gris\">Période : juin 2026</span>",
        ),
        (
            "La part patronale (jusqu'à 7,18 € par titre en 2025) est exonérée de cotisations et d'impôt sur le revenu.",
            "La part patronale (jusqu'à 7,32 € par titre en 2026) est exonérée de cotisations et d'impôt sur le revenu.",
        ),
    ],
    "article-219.html": [
        (
            "Exonérée jusqu'à 2× le plafond annuel SS (92 736 € en 2025)",
            "Exonérée jusqu'à 2× le plafond annuel SS (96 120 € en 2026)",
        ),
    ],
    "article-221.html": [
        (
            '<div class="decom-row"><span class="decom-label">Plafond journalier</span><span class="decom-val">53,49 €/jour (2025)</span></div>',
            '<div class="decom-row"><span class="decom-label">Plafond journalier</span><span class="decom-val">41,95 €/jour (depuis le 01/02/2026, suite à la réforme de 2025 abaissant la base de calcul de 1,8 à 1,4 SMIC)</span></div>',
        ),
    ],
    "article-222.html": [
        (
            "Les indemnités télétravail — montants 2025",
            "Les indemnités télétravail — montants 2026",
        ),
    ],
    "article-224.html": [
        (
            "Plafond par salarié</span><span class=\"comp-val\">75 % du PASS (32 994 € en 2025)</span>",
            "Plafond par salarié</span><span class=\"comp-val\">75 % du PASS (36 045 € en 2026)</span>",
        ),
        (
            "Il peut atteindre 300 % de votre versement, dans la limite de 8 % du PASS (environ 3 519 € en 2025).",
            "Il peut atteindre 300 % de votre versement, dans la limite de 8 % du PASS (environ 3 845 € en 2026).",
        ),
    ],
}


def main():
    total_fichiers = 0
    total_remplacements = 0

    for fichier, paires in REMPLACEMENTS.items():
        if not os.path.exists(fichier):
            print(f"❌ {fichier} introuvable, ignoré.")
            continue

        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()

        contenu_original = contenu
        nb_modifs_fichier = 0

        for ancien, nouveau in paires:
            if nouveau in contenu and ancien not in contenu:
                continue
            if ancien in contenu:
                contenu = contenu.replace(ancien, nouveau)
                nb_modifs_fichier += 1

        if nb_modifs_fichier == 0:
            print(f"✅ {fichier} : déjà corrigé ou texte non trouvé")
            continue

        ext = fichier.replace("article-", "").replace(".html", "")
        with open(fichier + f".bak_art{ext}", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")
    print(f"PASS 2026 = 48060e utilise comme reference pour tous les calculs")


if __name__ == "__main__":
    main()
