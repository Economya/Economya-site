#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du lot article-428/434/435/438/439/441/442/443/445
À lancer depuis ~/Desktop/mon site

article-439 : plafond PER TNS confirmé à 88 911€ pour 2026 (formule
Madelin, art. 154 bis CGI) — l'article citait 81 384€, valeur d'une
année antérieure.

article-434/435/438/445 : exemples illustratifs, années avancées d'un
an pour rester pertinents (mécanismes inchangés).
article-428/442/443 : dates génériques uniquement.
article-441 : référence historique correcte (Pinel terminé fin 2024),
non modifiée.

Idempotent. Sauvegardes individuelles .bak_artXXX.

Usage :
    python3 corriger_lot428_445.py
"""

import os

REMPLACEMENTS = {
    "article-428.html": [
        (
            "💡 Le meilleur produit zéro capital en 2025 : le template Notion",
            "💡 Le meilleur produit zéro capital en 2026 : le template Notion",
        ),
    ],
    "article-434.html": [
        (
            "vous pouvez déposer une réclamation contentieuse auprès de votre centre des impôts jusqu'à fin 2027 pour les erreurs sur la déclaration 2024.",
            "vous pouvez déposer une réclamation contentieuse auprès de votre centre des impôts jusqu'au 31 décembre de la 2e année suivant celle de la mise en recouvrement (délai standard de réclamation).",
        ),
    ],
    "article-435.html": [
        (
            "Si vos revenus de 2025 sont inférieurs à ceux de 2024 (chômage, temps partiel, reconversion), vous payez trop d'impôt à la source chaque mois.",
            "Si vos revenus de l'année en cours sont inférieurs à ceux de l'année précédente (chômage, temps partiel, reconversion), vous payez trop d'impôt à la source chaque mois.",
        ),
    ],
    "article-438.html": [
        (
            "📊 Exemple : appartement acheté 150 000 € en 2018, vendu 220 000 € en 2025 (7 ans)",
            "📊 Exemple : appartement acheté 150 000 € en 2019, vendu 220 000 € en 2026 (7 ans)",
        ),
    ],
    "article-439.html": [
        (
            "PER individuel uniquement (ou ex-Madelin transféré). Déduction très avantageuse : jusqu'à 81 384 € en 2025 pour les TNS. Puissant levier fiscal.",
            "PER individuel uniquement (ou ex-Madelin transféré). Déduction très avantageuse : jusqu'à 88 911 € en 2026 pour les TNS (formule Madelin, art. 154 bis CGI). Puissant levier fiscal.",
        ),
    ],
    "article-442.html": [
        (
            "📋 Micro-entrepreneur 2025",
            "📋 Micro-entrepreneur 2026",
        ),
        (
            "📊 Les taux de cotisations 2025",
            "📊 Les taux de cotisations 2026",
        ),
    ],
    "article-443.html": [
        (
            "💰 Les aides à la création d'entreprise en 2025",
            "💰 Les aides à la création d'entreprise en 2026",
        ),
    ],
    "article-445.html": [
        (
            "Avec moins de 10 % d'apport en 2025 (recommandation HCSF), l'accord de prêt est nettement plus difficile.",
            "Avec moins de 10 % d'apport (recommandation HCSF, toujours en vigueur en 2026), l'accord de prêt est nettement plus difficile.",
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
    print(f"⚠️ article-439: plafond PER TNS 81384e->88911e")


if __name__ == "__main__":
    main()
