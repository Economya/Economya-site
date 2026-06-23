#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction du bloc partenaire Fundora — ajout de l'avertissement de risque obligatoire
À lancer depuis ~/Desktop/mon site, sur tous les fichiers concernés

Fundora est une plateforme de private equity (investissement non coté).
Le site officiel de Fundora affiche systématiquement un avertissement de
risque de perte en capital. Notre texte "projets rentables" sans nuance
ni avertissement est un vrai problème de conformité, pas juste un style
à ajuster.

Idempotent. Sauvegarde en .bak_fundora.

Usage :
    python3 corriger_fundora.py
"""

import os
import glob

ANCIEN = 'Investissez facilement dans des projets rentables. Commencez dès 100€.'
NOUVEAU = 'Investissez dès 100€ dans des fonds de private equity sélectionnés. Investissement risqué : capital non garanti, liquidité limitée sur 6 à 10 ans.'


def traiter_fichier(chemin):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if NOUVEAU in contenu:
        return "déjà corrigé"

    if ANCIEN not in contenu:
        return None

    with open(chemin + ".bak_fundora", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(ANCIEN, NOUVEAU)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return "corrigé"


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    corriges = 0
    deja_ok = 0

    for fichier in fichiers:
        resultat = traiter_fichier(fichier)
        if resultat == "corrigé":
            corriges += 1
            print(f"✅ {fichier} : corrigé")
        elif resultat == "déjà corrigé":
            deja_ok += 1

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers corrigés : {corriges}")
    print(f"Déjà à jour : {deja_ok}")
    print(f"Sauvegardes créées avec l'extension .bak_fundora")


if __name__ == "__main__":
    main()
