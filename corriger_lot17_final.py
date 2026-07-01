#!/usr/bin/env python3
"""
Corrige 3 problemes trouves lors de l'audit qualite (lot 17) :

1. article-266.html (Leasing social VE) : seuil distance domicile-travail
   15 km -> 10 km (3e edition 2026, confirme service-public.gouv.fr).

2. article-261.html (Bonus ecologique) : seuil leasing social "15 400 €"
   -> 16 880 € (confirme jechangemavoiture.gouv.fr et service-public.gouv.fr).

3. article-69.html (Aides primo-accedants) : "en 2025" residuel, deja
   traite au lot 15 mais reconfirme ici au cas ou le fix precedent n'a
   pas ete applique correctement.

Idempotent. Sauvegardes .bak_lot17 avant modification.
"""

import os
import shutil

CORRECTIONS = {
    "article-266.html": [
        (
            "Trajets domicile-travail > 15 km OU pas de TC adaptés",
            "Trajets domicile-travail > 10 km OU plus de 8 000 km/an pro",
        ),
    ],
    "article-261.html": [
        (
            "Leasing social 100 € à 150 €/mois pour les éligibles (revenus ≤ 15 400 €)",
            "Leasing social 100 € à 150 €/mois pour les éligibles (revenus ≤ 16 880 €)",
        ),
        (
            "Si votre revenu fiscal de référence est inférieur à 15 400 €, le leasing social",
            "Si votre revenu fiscal de référence est inférieur à 16 880 €, le leasing social",
        ),
    ],
    "article-69.html": [
        (
            "Voici les principaux dispositifs à connaître en 2025.",
            "Voici les principaux dispositifs à connaître en 2026.",
        ),
    ],
}


def corriger_fichier(fichier, remplacements):
    if not os.path.exists(fichier):
        print(f"  Fichier introuvable : {fichier} (ignore)")
        return

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in remplacements:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            print(f"  OK Corrige : {ancien[:55]}...")
            total += 1
        elif nouveau in contenu_modifie:
            print(f"  INFO Deja corrige (idempotent) : {nouveau[:55]}...")
        else:
            print(f"  ATTENTION chaine non trouvee : {ancien[:55]}...")

    if total == 0:
        print(f"  -> Rien a faire pour {fichier}.")
        return

    shutil.copy2(fichier, fichier + ".bak_lot17")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  -> {total} correction(s) ecrite(s) dans {fichier} (sauvegarde creee)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
