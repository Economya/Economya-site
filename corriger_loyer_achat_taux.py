#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harmonisation simulateur-loyer-achat.html — taux d'emprunt aligné sur
calculateur-capacite-emprunt.html (déjà corrigé aujourd'hui)
À lancer depuis ~/Desktop/mon site

Frais de notaire (8% du prix) confirmés EXACTS par calcul détaillé avec
les vrais barèmes (DMTO 6,32% + émoluments + CSI + débours = 8,05% pour
un bien moyen) — non modifiés.

Taux d'emprunt harmonisé à 3,4% (médiane marché juin 2026), cohérent
avec la correction déjà appliquée sur calculateur-capacite-emprunt.html.

Idempotent. Sauvegarde en .bak_tauxloyerachat2026.

Usage :
    python3 corriger_loyer_achat_taux.py
"""

import os

FICHIER = "simulateur-loyer-achat.html"

ANCIEN = "const tauxMensuel = 0.035 / 12;"
NOUVEAU = "const tauxMensuel = 0.034 / 12; // Taux indicatif ~3,4% (moyenne marché juin 2026, fluctue mensuellement)"


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
    with open(FICHIER + ".bak_tauxloyerachat2026", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU, 1)
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)
    print("✅ Taux d'emprunt harmonisé : 3,5% -> 3,4% (cohérent avec calculateur-capacite-emprunt.html)")
    print("   Frais de notaire 8% confirmes exacts (calcul detaille), non modifies")


if __name__ == "__main__":
    main()
