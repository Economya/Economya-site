#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction checklist-abonnements.html — prix Netflix obsolètes
À lancer depuis ~/Desktop/mon site

MÊME ERREUR que celle trouvée et corrigée dans les articles du site ce
matin : tous les tarifs Netflix ont augmenté en janvier 2026. Confirmé
par sources convergentes (Selectra, Echos du Net, juin 2026) :
- Standard avec pub : 4,99€ -> 7,99€
- Standard (sans pub) : 13,49€ -> 14,99€
- Premium : non présent dans l'outil, pour info 21,99€

Idempotent. Sauvegarde en .bak_netflixabos2026.

Usage :
    python3 corriger_checklist_abos_netflix.py
"""

import os

FICHIER = "checklist-abonnements.html"

REMPLACEMENTS = [
    (
        "{ nom: 'Netflix', detail: 'Standard sans pub', prix: 13.49 },",
        "{ nom: 'Netflix', detail: 'Standard sans pub', prix: 14.99 },",
    ),
    (
        "{ nom: 'Netflix', detail: 'Avec publicités', prix: 4.99 },",
        "{ nom: 'Netflix', detail: 'Avec publicités', prix: 7.99 },",
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
        print("✅ Déjà corrigé ou texte non trouvé.")
        return

    with open(FICHIER + ".bak_netflixabos2026", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} prix Netflix corrigé(s) : 13,49€->14,99€ et 4,99€->7,99€")


if __name__ == "__main__":
    main()
