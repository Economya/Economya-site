#!/usr/bin/env python3
"""
Corrige 2 problèmes trouvés lors de l'audit qualité (lot 9) :

1. article-277.html : la balise <title> disait "Interrail 2025" alors que
   og:title, twitter:title et le vrai H1 disent tous "Interrail 2026".
   C'est cette balise <title> incohérente qui a servi de référence à notre
   script corriger_simcard_titres.py, propageant "2025" dans 13+ fichiers
   via le widget "Articles similaires". Une fois corrigée ici, il faudra
   relancer corriger_simcard_titres.py pour propager "2026" partout.

2. article-49.html (Sorties en famille) : affirme que "Le Louvre, Orsay,
   le Centre Pompidou… tous gratuits... le premier dimanche du mois".
   Faux sur 2 points (déjà vérifiés lot 3) :
   - Le Louvre n'est plus gratuit le dimanche depuis 2014 (gratuité
     supprimée) ; son vrai jour gratuit est le 1er vendredi soir.
   - Le Centre Pompidou est fermé pour travaux jusqu'en 2030.

Idempotent. Sauvegardes .bak_auditqualite_lot9 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-277.html": [
        (
            "<title>Interrail 2025 : guide complet Europe en train — Economya.fr</title>",
            "<title>Interrail 2026 : guide complet Europe en train — Economya.fr</title>",
        ),
    ],
    "article-49.html": [
        (
            "<h3>Les musées nationaux le premier dimanche du mois</h3><p>Le Louvre, Orsay, le Centre Pompidou… tous gratuits pour tout le monde le premier dimanche du mois. Planifiez à l'avance.</p>",
            "<h3>Les musées nationaux gratuits</h3><p>Orsay et le musée de Cluny sont gratuits le premier dimanche du mois. Le Louvre est gratuit le premier vendredi soir (18h-21h45, hors juillet-août). Le Centre Pompidou est actuellement fermé pour travaux jusqu'en 2030. Planifiez à l'avance.</p>",
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

    shutil.copy2(fichier, fichier + ".bak_auditqualite_lot9")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  → {total} correction(s) écrite(s) dans {fichier} (sauvegarde créée)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
