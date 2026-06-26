#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des dates 2025->2026 sur 4 fichiers (lot 226-247)
À lancer depuis ~/Desktop/mon site

article-226 : exonération heures sup (7 500€/an) confirmée stable et
inchangée pour 2026 (malgré débats parlementaires) — seules les dates
sont corrigées, pas le dispositif lui-même.
article-237/245/247 : contenu générique, dates uniquement.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot226_247.py
"""

import os

REMPLACEMENTS = {
    "article-226.html": [
        (
            "En 2025, les heures supplémentaires bénéficient d'une exonération fiscale et sociale particulièrement avantageuse.",
            "En 2026, les heures supplémentaires bénéficient toujours d'une exonération fiscale et sociale particulièrement avantageuse (plafond de 7 500€/an confirmé inchangé malgré les débats parlementaires).",
        ),
        (
            "L'avantage fiscal 2025 — exonération élargie",
            "L'avantage fiscal 2026 — exonération élargie",
        ),
    ],
    "article-237.html": [
        (
            "📱 Les meilleures plateformes en 2025",
            "📱 Les meilleures plateformes en 2026",
        ),
    ],
    "article-245.html": [
        (
            "📋 Guide complet 2025",
            "📋 Guide complet 2026",
        ),
    ],
    "article-247.html": [
        (
            "En 2025, l'intelligence artificielle peut analyser vos factures, négocier vos abonnements, comparer des prix en temps réel et optimiser votre budget — souvent gratuitement.",
            "L'intelligence artificielle peut analyser vos factures, négocier vos abonnements, comparer des prix en temps réel et optimiser votre budget — souvent gratuitement.",
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


if __name__ == "__main__":
    main()
