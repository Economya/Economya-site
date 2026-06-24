#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction flat tax/PFU 30% -> 31,4% pour les produits CONCERNÉS par la
hausse de CSG du 1er janvier 2026 (loi n°2025-1403)
À lancer depuis ~/Desktop/mon site

⚠️ Ne concerne QUE : crypto, PEA (avant 5 ans), dividendes/intérêts génériques.
NE TOUCHE PAS : article-337 (PEL, exempté, reste à 30%), article-340
(assurance-vie succession, régime art. 990 I différent), article-385
(régime fiscal portugais, hors sujet).

Idempotent. Sauvegarde en .bak_flattax avant modification.

Usage :
    python3 corriger_flattax_lot1.py
"""

import os

REMPLACEMENTS = {
    "article-158.html": [
        (
            "En France, les plus-values crypto sont imposées à 30 % (flat tax) dès le premier euro de cession vers des euros.",
            "En France, les plus-values crypto sont imposées à 31,4 % (flat tax, depuis le 1er janvier 2026) dès le premier euro de cession vers des euros.",
        ),
    ],
    "article-344.html": [
        (
            "En France, les plus-values sur cession de cryptomonnaies sont soumises à la flat tax de 30 % (ou barème progressif sur option).",
            "En France, les plus-values sur cession de cryptomonnaies sont soumises à la flat tax de 31,4 % depuis 2026 (ou barème progressif sur option).",
        ),
    ],
    "article-338.html": [
        (
            'Les plus-values sont alors soumises à la flat tax (30 %).',
            'Les plus-values sont alors soumises à la flat tax (31,4 % depuis 2026).',
        ),
    ],
    "article-339.html": [
        (
            "Plus-values soumises à la flat tax complète de 30 % (12,8 % IR + 17,2 % prélèvements sociaux).",
            "Plus-values soumises à la flat tax complète de 31,4 % depuis 2026 (12,8 % IR + 18,6 % prélèvements sociaux).",
        ),
        (
            "Un retrait avant 5 ans clôture automatiquement le PEA et déclenche la flat tax (30 %).",
            "Un retrait avant 5 ans clôture automatiquement le PEA et déclenche la flat tax (31,4 % depuis 2026).",
        ),
    ],
    "article-474.html": [
        (
            '<strong>Fiscalité défavorable — flat tax 30 %</strong><span>Les intérêts perçus sont soumis au PFU (flat tax) de 30 %. Un rendement affiché de 10 % devient ~7 % net après flat tax. Comparez toujours les rendements nets et non bruts.</span>',
            '<strong>Fiscalité défavorable — flat tax 31,4 %</strong><span>Les intérêts perçus sont soumis au PFU (flat tax) de 31,4 % depuis 2026. Un rendement affiché de 10 % devient ~6,9 % net après flat tax. Comparez toujours les rendements nets et non bruts.</span>',
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

        with open(fichier + ".bak_flattax", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")
    print(f"⚠️ NON touchés (volontairement) : article-337 (PEL, exempté),")
    print(f"   article-340 (régime succession différent), article-385 (Portugal)")


if __name__ == "__main__":
    main()
