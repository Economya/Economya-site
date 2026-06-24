#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-47.html — taux MaPrimeRénov' et nuance isolation combles
À lancer depuis ~/Desktop/mon site

1. Dates 2025 -> 2026
2. "Jusqu'à 70% du coût" -> "jusqu'à 80%" (cohérent avec le taux maximum
   2026 confirmé sur les autres articles déjà corrigés)
3. Mention "isolation combles" : ajout d'une note de clarification — la
   prime au m² reste possible pour les combles aménagés/rampants de
   toiture, mais les combles PERDUS sont exclus du parcours par geste
   depuis le 1er janvier 2026 (nécessitent une rénovation d'ampleur).
   Le montant "5 000€" lui-même n'est pas modifié (plausible selon
   surface réelle, mais sources partiellement contradictoires sur le
   sujet — prudence maintenue).

Idempotent. Sauvegarde en .bak_art47.

Usage :
    python3 corriger_article47.py
"""

import os

FICHIER = "article-47.html"

REMPLACEMENTS = [
    (
        "MaPrimeRénov', l'Éco-PTZ (prêt à taux zéro), les CEE (Certificats d'Économies d'Énergie), la TVA à 5,5% et les aides des collectivités locales peuvent couvrir 30 à 70% du coût de travaux de rénovation énergétique. Ces aides doivent être demandées AVANT le début des travaux — jamais après. Un conseiller France Rénov' (gratuit, service public) peut vous guider dans le montage du dossier.",
        "MaPrimeRénov', l'Éco-PTZ (prêt à taux zéro), les CEE (Certificats d'Économies d'Énergie), la TVA à 5,5% et les aides des collectivités locales peuvent couvrir 30 à 80% du coût de travaux de rénovation énergétique selon vos revenus et le type de travaux. ⚠️ Depuis 2026, certains travaux (isolation des murs, chaudières biomasse, combles perdus) ne sont finançables que via une rénovation d'ampleur, pas en geste isolé. Ces aides doivent être demandées AVANT le début des travaux — jamais après. Un conseiller France Rénov' (gratuit, service public) peut vous guider dans le montage du dossier.",
    ),
    (
        "Les aides financières disponibles en 2025",
        "Les aides financières disponibles en 2026",
    ),
    (
        "Jusqu'à 70% du coût",
        "Jusqu'à 80% du coût",
    ),
    (
        "<span>MaPrimeRénov' (isolation combles 5 000€, ménage modeste)</span><span>-2 500 à -4 000€</span>",
        "<span>MaPrimeRénov' (isolation rampants/combles aménagés, ménage modeste)</span><span>-2 500 à -4 000€</span>",
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

    with open(FICHIER + ".bak_art47", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Taux 70%->80%, précision combles aménagés vs perdus, dates 2026")


if __name__ == "__main__":
    main()
