#!/usr/bin/env python3
"""
Corrige 2 erreurs factuelles trouvées lors de l'audit qualité (lot 3) :

1. article-403.html (Musées gratuits) :
   - Musée d'Orsay : "premier jeudi" est faux, le jour de gratuité réel est
     le premier DIMANCHE du mois (toute la journée, réservation obligatoire).
     Le jeudi soir à Orsay est une nocturne PAYANTE (12€), pas gratuite.
   - Centre Pompidou : fermé pour travaux de 2025 à 2030, information absente
     de l'article alors qu'il est présenté comme visitable.

2. article-263.html (Malus écologique) :
   - Seuil d'exemption "0 à 117 g" est le seuil 2024, obsolète.
     Seuil réel 2026 (confirmé multi-sources, L'Argus/service-public) : 108 g/km,
     donc la tranche exemptée est "0 à 107 g".

Idempotent. Sauvegardes .bak_auditqualite_lot3 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-403.html": [
        (
            "Gratuit le premier jeudi de chaque mois de 18h à 21h45. Gratuit pour les moins de 18 ans et les 18–25 ans résidents UE. Tarif plein : 16 €.",
            "Gratuit le premier dimanche de chaque mois (réservation obligatoire). Gratuit pour les moins de 18 ans et les 18–25 ans résidents UE. Tarif plein : 16 €.",
        ),
        (
            "<h3>Centre Pompidou</h3>",
            "<h3>Centre Pompidou ⚠️ fermé pour travaux jusqu'en 2030</h3>",
        ),
    ],
    "article-263.html": [
        (
            '<tr><td>0 à 117 g</td><td class="g">0 €</td><td class="g">0 €</td></tr>',
            '<tr><td>0 à 107 g</td><td class="g">0 €</td><td class="g">0 €</td></tr>',
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

    shutil.copy2(fichier, fichier + ".bak_auditqualite_lot3")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  → {total} correction(s) écrite(s) dans {fichier} (sauvegarde créée)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
