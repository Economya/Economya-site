#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-203.html — PTZ : dates 2025->2026
À lancer depuis ~/Desktop/mon site

Confirmé stable pour 2026 (sources multiples convergentes) : zones et
taux (50%/40%/40%), extension maisons neuves en zone C, prorogation
jusqu'au 31/12/2027. Les dates "2025" sont mises à jour en "2026".

⚠️ Plafonds de revenus précis : sources contradictoires sur une éventuelle
revalorisation +8 à 13% en 2026 (une source confirme exactement les
mêmes montants que l'article, d'autres annoncent une hausse). Par
prudence, les chiffres ne sont PAS modifiés mais une note de vérification
est ajoutée plutôt que de deviner.

Idempotent. Sauvegarde en .bak_art203.

Usage :
    python3 corriger_article203.py
"""

import os

FICHIER = "article-203.html"

REMPLACEMENTS = [
    (
        "PTZ 2025 : conditions, simulation, communes éligibles — Jusqu'à 100 000€ sans intérêts. Guide complet sur Economya.fr",
        "PTZ 2026 : conditions, simulation, communes éligibles — Jusqu'à 100 000€ sans intérêts. Guide complet sur Economya.fr",
    ),
    (
        "PTZ 2025 : conditions, simulation, communes éligibles — Economya.fr",
        "PTZ 2026 : conditions, simulation, communes éligibles — Economya.fr",
    ),
    (
        '"headline": "PTZ 2025 : conditions, simulation, communes éligibles",',
        '"headline": "PTZ 2026 : conditions, simulation, communes éligibles",',
    ),
    (
        "<h1>PTZ 2025 : conditions, simulation, communes éligibles</h1>",
        "<h1>PTZ 2026 : conditions, simulation, communes éligibles</h1>",
    ),
    (
        '<meta property="og:title" content="PTZ 2025 : conditions, simulation, communes éligibles">',
        '<meta property="og:title" content="PTZ 2026 : conditions, simulation, communes éligibles">',
    ),
    (
        '<meta name="twitter:title" content="PTZ 2025 : conditions, simulation, communes éligibles">',
        '<meta name="twitter:title" content="PTZ 2026 : conditions, simulation, communes éligibles">',
    ),
    (
        "Le Prêt à Taux Zéro (PTZ) est l'aide à l'accession la plus puissante de l'État — et l'une des moins bien utilisées. En 2025, il a été profondément réformé : élargi aux maisons individuelles neuves dans toutes les zones, reconduit jusqu'en 2027, plafonds de revenus relevés. Résultat : beaucoup plus de ménages sont éligibles qu'ils ne le pensent. Voici tout ce qu'il faut savoir avant de déposer un dossier.",
        "Le Prêt à Taux Zéro (PTZ) est l'aide à l'accession la plus puissante de l'État — et l'une des moins bien utilisées. Depuis sa réforme d'avril 2025 (élargissement aux maisons individuelles neuves dans toutes les zones), le dispositif reste stable et reconduit jusqu'au 31 décembre 2027. ⚠️ Les plafonds de revenus font l'objet de discussions de revalorisation en 2026 — vérifiez les montants exacts sur le simulateur officiel service-public.fr avant de monter votre dossier. Voici tout ce qu'il faut savoir avant de déposer un dossier.",
    ),
    (
        "Plafonds de revenus 2025 (revenu fiscal N-2)",
        "Plafonds de revenus 2026 (revenu fiscal N-2) — à vérifier sur le simulateur officiel",
    ),
    (
        "📌 Nouveauté 2025 : maisons individuelles en zone C",
        "📌 Depuis 2025 : maisons individuelles en zone C",
    ),
    (
        "Depuis le 1er janvier 2025, les maisons individuelles neuves sont à nouveau éligibles au PTZ en zone C",
        "Depuis le 1er janvier 2025, et toujours en vigueur en 2026, les maisons individuelles neuves sont éligibles au PTZ en zone C",
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

    with open(FICHIER + ".bak_art203", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Dates 2026, note prudence plafonds ajoutee")


if __name__ == "__main__":
    main()
