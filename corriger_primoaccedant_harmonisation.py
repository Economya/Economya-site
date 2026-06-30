#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harmonisation primo-accedant.html — taux d'emprunt et frais de notaire
À lancer depuis ~/Desktop/mon site

1. Taux d'emprunt : 3,5% -> 3,4%, harmonisé avec les corrections déjà
   appliquées aujourd'hui sur calculateur-capacite-emprunt.html et
   simulateur-loyer-achat.html (médiane marché juin 2026).
2. Frais de notaire ancien : 7,5% -> 8%, harmonisé avec le calcul
   détaillé confirmé aujourd'hui (DMTO 6,32% + émoluments + CSI +
   débours = 8,05% pour un bien moyen, cf. simulateur-loyer-achat.html
   et calculateur-frais-notaire.html). 2 occurrences dans ce fichier.

Idempotent. Sauvegarde en .bak_primoaccedant avant modification.

Usage :
    python3 corriger_primoaccedant_harmonisation.py
"""

import os

FICHIER = "primo-accedant.html"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    # 1. Taux d'emprunt
    ancien_taux = "const taux = 0.035; // 3,5% en 2026"
    nouveau_taux = "const taux = 0.034; // 3,4% en 2026 (harmonise avec les autres outils)"
    if nouveau_taux in contenu:
        pass
    elif ancien_taux in contenu:
        contenu = contenu.replace(ancien_taux, nouveau_taux, 1)
        nb_modifs += 1
    else:
        print(f"⚠️  Taux non trouvé (ignoré).")

    # 2. Frais de notaire ancien (toutes occurrences : 0.075 -> 0.08)
    ancien_fn = "Math.round(data.prix * (data.typeBien === 'neuf' ? 0.025 : 0.075))"
    nouveau_fn = "Math.round(data.prix * (data.typeBien === 'neuf' ? 0.025 : 0.08))"
    nb_fn = contenu.count(ancien_fn)
    if nb_fn > 0:
        contenu = contenu.replace(ancien_fn, nouveau_fn)
        nb_modifs += nb_fn
        print(f"   {nb_fn} occurrence(s) de frais de notaire corrigee(s)")

    # 3. Montant emprunte (qui ajoute aussi les frais de notaire dans le calcul)
    ancien_me = "Math.round(data.prix * 0.075)"
    nouveau_me = "Math.round(data.prix * 0.08)"
    if ancien_me in contenu:
        contenu = contenu.replace(ancien_me, nouveau_me, 1)
        nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé.")
        return

    with open(FICHIER + ".bak_primoaccedant", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} correction(s) appliquee(s) dans primo-accedant.html")
    print("   - Taux d'emprunt: 3,5% -> 3,4%")
    print("   - Frais de notaire ancien: 7,5% -> 8% (harmonise)")


if __name__ == "__main__":
    main()
