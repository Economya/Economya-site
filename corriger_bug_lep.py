#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du bug de calcul LEP dans comparateur-livrets.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Bug identifié : le calcul du gain LEP utilisait encore 4% (ancien taux),
alors que le taux affiché dans le tableau est bien 2,5% (taux officiel
en vigueur depuis le 1er février 2026). Incohérence interne corrigée.

Sans danger à relancer (idempotent). Sauvegarde en .bak_lep avant modification.

Usage :
    python3 corriger_bug_lep.py
"""

import os

FICHIER = "comparateur-livrets.html"

ANCIEN_CALCUL = "const gainLEP = Math.min(montant, 10000) * 4 / 100;"
NOUVEAU_CALCUL = "const gainLEP = Math.min(montant, 10000) * 2.5 / 100;"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable dans ce dossier.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if NOUVEAU_CALCUL in contenu:
        print("✅ Déjà corrigé — taux LEP cohérent (2,5%).")
        return

    if ANCIEN_CALCUL not in contenu:
        print("⚠️  La ligne attendue n'a pas été trouvée telle quelle.")
        print("   Aucune modification effectuée, pour éviter une erreur.")
        return

    with open(FICHIER + ".bak_lep", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(ANCIEN_CALCUL, NOUVEAU_CALCUL, 1)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    print("✅ Bug corrigé : le calcul du gain LEP utilise maintenant 2,5% (taux officiel),")
    print("   cohérent avec le taux affiché dans le tableau comparatif.")
    print(f"   Sauvegarde créée : {FICHIER}.bak_lep")


if __name__ == "__main__":
    main()
