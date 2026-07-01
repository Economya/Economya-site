#!/usr/bin/env python3
"""
Corrige 2 problèmes trouvés lors de l'audit qualité (lot 6) :

1. article-403.html (Musées gratuits) : résidu de notre correction du lot 3.
   La phrase principale sur Orsay dit déjà "premier dimanche" (corrigée),
   mais les badges/pastilles juste en dessous disaient encore "1er jeudi".

2. article-492.html (Néobanques) : le fil d'Ariane (+ son JSON-LD) affichait
   "quelle néobanque en 2025" alors que le vrai H1 de l'article dit "2026".

Idempotent. Sauvegardes .bak_auditqualite_lot6 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-403.html": [
        (
            '<span class="mtag g">Gratuit 1er jeudi du mois (soir)</span><span class="mtag g">Gratuit -26 ans UE</span>',
            '<span class="mtag g">Gratuit 1er dimanche du mois</span><span class="mtag g">Gratuit -26 ans UE</span>',
        ),
        (
            '<span class="m-tarif">0 € possible</span><span class="m-sub">1er jeudi soir</span>',
            '<span class="m-tarif">0 € possible</span><span class="m-sub">1er dimanche</span>',
        ),
    ],
    "article-492.html": [
        (
            '<span style="color:var(--t,#2C2C2A)">Revolut, N26, Lydia : quelle néobanque en 2025</span></div>',
            '<span style="color:var(--t,#2C2C2A)">Revolut, N26, Lydia : quelle néobanque en 2026</span></div>',
        ),
        (
            '{"@type": "ListItem", "position": 3, "name": "Revolut, N26, Lydia : quelle néobanque en 2025", "item": "https://economya.fr/article-492.html"}',
            '{"@type": "ListItem", "position": 3, "name": "Revolut, N26, Lydia : quelle néobanque en 2026", "item": "https://economya.fr/article-492.html"}',
        ),
    ],
}


def corriger_fichier(fichier, remplacements):
    if not os.path.exists(fichier):
        print(f"❌ Fichier introuvable : {fichier} (ignoré)")
        return

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in remplacements:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            print(f"  ✅ Corrigé : {ancien[:55]}...")
            total += 1
        elif nouveau in contenu_modifie:
            print(f"  ℹ️  Déjà corrigé (idempotent) : {nouveau[:55]}...")
        else:
            print(f"  ⚠️  Chaîne non trouvée : {ancien[:55]}...")

    if total == 0:
        print(f"  → Rien à faire pour {fichier}.")
        return

    shutil.copy2(fichier, fichier + ".bak_auditqualite_lot6")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  → {total} correction(s) écrite(s) dans {fichier} (sauvegarde créée)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
