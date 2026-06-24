#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction "Boursorama" -> "BoursoBank" (rebranding officiel depuis le
2 octobre 2023) sur les articles qui désignent la banque en ligne
À lancer depuis ~/Desktop/mon site

Cible précisément article-51.html, article-82.html et article-174.html
(les 3 cas confirmés en contexte de banque, sans ambiguïté). N'altère PAS
article-491.html ("Boursorama Shop", nom de programme cashback non
vérifié séparément) ni article-187/338.html (déjà corrects, disent déjà
"Boursobank (ex-Boursorama)").

Idempotent. Sauvegarde en .bak_boursobank.

Usage :
    python3 corriger_boursobank.py
"""

import os

REMPLACEMENTS = {
    "article-51.html": [
        ("<h3>Boursorama Banque</h3>", "<h3>BoursoBank</h3>"),
    ],
    "article-82.html": [
        ("<h3>Boursorama / Fortuneo</h3>", "<h3>BoursoBank / Fortuneo</h3>"),
    ],
    "article-174.html": [
        (
            "Boursorama, Fortuneo ou BourseDirectouvrent un PEA gratuitement.",
            "BoursoBank, Fortuneo ou BourseDirect ouvrent un PEA gratuitement.",
        ),
    ],
}


def main():
    total_fichiers = 0
    total_remplacements = 0

    for fichier, paires in REMPLACEMENTS.items():
        if not os.path.exists(fichier):
            print(f"❌ {fichier} introuvable, ignoré.")
            continue

        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()

        contenu_original = contenu
        nb_modifs_fichier = 0

        for ancien, nouveau in paires:
            if nouveau in contenu and ancien not in contenu:
                continue
            if ancien in contenu:
                contenu = contenu.replace(ancien, nouveau)
                nb_modifs_fichier += 1

        if nb_modifs_fichier == 0:
            print(f"✅ {fichier} : déjà corrigé ou texte non trouvé")
            continue

        with open(fichier + ".bak_boursobank", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")
    print(f"⚠️ article-491.html ('Boursorama Shop') volontairement non touché")
    print(f"   (nom de programme cashback non vérifié séparément)")


if __name__ == "__main__":
    main()
