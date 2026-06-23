#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de finitions diverses
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

1. Retire le bloc "Partager cet article" sur mentions-legales.html et
   politique-confidentialite.html (n'a pas de sens sur des pages légales)
2. Corrige "ne influence" -> "n'influence" (faute de grammaire)
3. Corrige "l audience" -> "l'audience" dans le bandeau cookies, sur TOUS
   les fichiers HTML (apostrophe manquante détectée)

Idempotent. Sauvegardes en .bak_finitions avant modification.

Usage :
    python3 corriger_finitions.py
"""

import os
import re
import glob

PATTERN_PARTAGE = re.compile(
    r"<!-- Boutons partage -->.*?</script>\s*\n",
    re.DOTALL
)


def retirer_partage(fichier):
    if not os.path.exists(fichier):
        return "introuvable"
    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if "Partager cet article" not in contenu:
        return "déjà absent"
    nouveau = PATTERN_PARTAGE.sub("", contenu, count=1)
    if nouveau == contenu:
        return "motif non trouvé"
    with open(fichier + ".bak_finitions", 'w', encoding='utf-8') as f:
        f.write(contenu)
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    return "retiré"


def corriger_grammaire(fichier):
    if not os.path.exists(fichier):
        return "introuvable"
    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if "n'influence" in contenu:
        return "déjà corrigé"
    if "ne influence" not in contenu:
        return "motif absent"
    nouveau = contenu.replace("ne influence", "n'influence")
    with open(fichier + ".bak_finitions", 'a', encoding='utf-8') as f:
        f.write(contenu)
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    return "corrigé"


def corriger_apostrophe_globale():
    fichiers = sorted(glob.glob("*.html")) + sorted(glob.glob("article-*.html"))
    fichiers = sorted(set(fichiers))
    corriges = 0
    deja_ok = 0
    for fichier in fichiers:
        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
        if "mesurer l'audience" in contenu:
            deja_ok += 1
            continue
        if "mesurer l audience" not in contenu:
            continue
        nouveau = contenu.replace("mesurer l audience", "mesurer l'audience")
        bak = fichier + ".bak_finitions"
        if not os.path.exists(bak):
            with open(bak, 'w', encoding='utf-8') as f:
                f.write(contenu)
        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(nouveau)
        corriges += 1
    return corriges, deja_ok


def main():
    print("=== 1. Retrait du bloc partage sur les pages légales ===")
    print(f"mentions-legales.html : {retirer_partage('mentions-legales.html')}")
    print(f"politique-confidentialite.html : {retirer_partage('politique-confidentialite.html')}")

    print("\n=== 2. Correction grammaire 'ne influence' -> 'n'influence' ===")
    print(f"mentions-legales.html : {corriger_grammaire('mentions-legales.html')}")

    print("\n=== 3. Correction apostrophe 'l audience' -> 'l'audience' (tous fichiers) ===")
    corriges, deja_ok = corriger_apostrophe_globale()
    print(f"Fichiers corrigés : {corriges}")
    print(f"Déjà corrects : {deja_ok}")


if __name__ == "__main__":
    main()
