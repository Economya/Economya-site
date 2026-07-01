#!/usr/bin/env python3
"""
Corrige article-237.html (Téléconsultation médicale gratuite) :

Le tarif "26,50 €" est l'ancien tarif de consultation généraliste, remplacé
par 30 € depuis le 22 décembre 2024 (source Ameli.fr / info.gouv.fr). Ce même
chiffre obsolète avait déjà été corrigé ailleurs sur le site (vrai-ou-faux.html)
-> incohérence interne à corriger ici aussi.

Précision supplémentaire : le tarif spécifique de la téléconsultation
généraliste est actuellement de 25 € (distinct du tarif de consultation
physique de 30 €), donc la phrase est reformulée pour être exacte sur les
deux tarifs.

Idempotent. Sauvegarde .bak_teleconsultation avant modification.
"""

import os
import shutil

FICHIER = "article-237.html"

ANCIEN = "Depuis 2022, la téléconsultation est remboursée <strong>au même tarif qu'une consultation classique</strong> (26,50 € par la Sécu, le reste par votre mutuelle). Deux conditions pour être pris en charge à 100 % :"

NOUVEAU = "Depuis 2022, la téléconsultation est remboursée par la Sécu sur la base de <strong>25 €</strong> (contre 30 € pour une consultation classique en cabinet depuis décembre 2024), le reste pouvant être pris en charge par votre mutuelle. Deux conditions pour être pris en charge à 100 % :"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    if NOUVEAU in contenu:
        print("✅ Rien à faire — déjà corrigé (idempotent).")
        return

    if ANCIEN not in contenu:
        print("⚠️  Chaîne attendue non trouvée. Vérifiez manuellement.")
        return

    contenu_modifie = contenu.replace(ANCIEN, NOUVEAU, 1)

    shutil.copy2(FICHIER, FICHIER + ".bak_teleconsultation")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"✅ 1 correction appliquée dans {FICHIER}")
    print(f"   26,50 € (obsolète) -> 25 € téléconsultation / 30 € consultation classique")
    print(f"   Sauvegarde créée : {FICHIER}.bak_teleconsultation")


if __name__ == "__main__":
    main()
