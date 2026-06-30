#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction calculateur-capacite-emprunt.html — taux d'emprunt légèrement
ajusté au consensus du marché (juin 2026)
À lancer depuis ~/Desktop/mon site

Taux d'endettement max 35% confirmé EXACT (recommandation HCSF en
vigueur, déjà vérifié plus tôt aujourd'hui).

Taux d'emprunt immobilier : très fort consensus (CAFPI, Pretto,
Meilleurtaux, Empruntis, tous datés fin juin 2026) autour de 3,37-3,47%
sur 20 ans. L'outil utilisait 3,5%, légèrement haut. Ajusté à 3,4%
(médiane des sources), avec note que ce taux est par nature TRÈS
volatil (change chaque mois) — contrairement aux barèmes CAF/fiscaux,
aucune "vraie" valeur unique n'existe ici.

Idempotent. Sauvegarde en .bak_tauximmo2026.

Usage :
    python3 corriger_capacite_emprunt_taux.py
"""

import os

FICHIER = "calculateur-capacite-emprunt.html"

ANCIEN = "const tauxMensuel = 0.035 / 12;"
NOUVEAU = "const tauxMensuel = 0.034 / 12; // Taux indicatif ~3,4% (moyenne marché juin 2026, fluctue mensuellement - vérifiez les taux actuels avant simulation réelle)"


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
    with open(FICHIER + ".bak_tauximmo2026", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Taux d'emprunt ajusté : 3,5% -> 3,4% (médiane des sources juin 2026)")
    print("   Taux d'endettement max 35% confirme deja exact, non modifie")


if __name__ == "__main__":
    main()
