#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction checklist-abonnements.html — prix Disney+ obsolète
À lancer depuis ~/Desktop/mon site

Disney+ Standard confirmé à 9,99€/mois (sources convergentes, juin
2026) — l'outil affichait 11,99€.

Apple TV+ (9,99€) et Prime Video (6,99€) déjà confirmés exacts dans
l'outil, non modifiés. Canal+ "Tous programmes" non corrigé : trop de
formules différentes (19,99€ à 39,99€ selon l'offre) pour trancher
avec certitude le montant affiché.

Idempotent. Sauvegarde en .bak_disneyabos2026.

Usage :
    python3 corriger_checklist_abos_disney.py
"""

import os

FICHIER = "checklist-abonnements.html"

ANCIEN = "{ nom: 'Disney+', detail: 'Standard', prix: 11.99 },"
NOUVEAU = "{ nom: 'Disney+', detail: 'Standard', prix: 9.99 },"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVEAU in contenu:
        print("✅ Déjà corrigé.")
        return
    if ANCIEN not in contenu:
        print("⚠️ Texte attendu non trouvé. Aucune modification.")
        return
    with open(FICHIER + ".bak_disneyabos2026", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Prix Disney+ corrigé : 11,99€ -> 9,99€")


if __name__ == "__main__":
    main()
