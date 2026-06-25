#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synchronisation des liens croisés (sim-card-title) avec le VRAI titre
actuel de chaque article cible (lu depuis son <h1>)
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Problème corrigé : quand un article est mis à jour (ex: "...2025" devient
"...2026" dans son propre <h1>), les LIENS CROISÉS depuis d'autres
articles vers lui ("Articles similaires") gardaient l'ancien texte
"...2025" — un texte de lien périmé, indépendant du contenu réel de la
page cible.

Méthode :
1. Lit le <h1> réel de chaque article-*.html -> construit un dictionnaire
   {nom_fichier: titre_actuel_nettoyé}
2. Parcourt tous les sim-card (liens croisés) de tous les articles, et
   remplace le texte du lien par le titre actuel de sa cible — UNIQUEMENT
   si le texte actuel du lien diffère ET contient une année (2024/2025)
   pour limiter les remplacements aux cas réellement périmés.

Idempotent. Sauvegarde en .bak_synctitles avant modification.

Usage :
    python3 synchroniser_liens_croises.py
"""

import os
import re
import glob

PATTERN_H1 = re.compile(r'<h1>(.*?)</h1>', re.DOTALL)
PATTERN_SIMCARD = re.compile(
    r'(<a class="sim-card" href="(article-\d+\.html)"><div class="sim-card-cat">[^<]*</div><div class="sim-card-title">)([^<]*)(</div></a>)'
)


def nettoyer_titre(titre_html):
    texte = re.sub(r'<[^>]+>', ' ', titre_html)
    texte = re.sub(r'\s+', ' ', texte).strip()
    return texte


def construire_dictionnaire_titres(fichiers):
    titres = {}
    for chemin in fichiers:
        with open(chemin, 'r', encoding='utf-8') as f:
            contenu = f.read()
        match = PATTERN_H1.search(contenu)
        if match:
            nom_fichier = os.path.basename(chemin)
            titres[nom_fichier] = nettoyer_titre(match.group(1))
    return titres


def traiter_fichier(chemin, titres):
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    def remplacer(match):
        nonlocal nb_modifs
        prefixe, cible, texte_actuel, suffixe = match.groups()
        titre_reel = titres.get(cible)
        if not titre_reel:
            return match.group(0)
        if texte_actuel == titre_reel:
            return match.group(0)
        # Ne remplacer que si le texte actuel contient une annee datee
        # (2023/2024/2025) pour limiter aux cas vraiment perimes
        if not re.search(r'202[3-5]', texte_actuel):
            return match.group(0)
        nb_modifs += 1
        return prefixe + titre_reel + suffixe

    nouveau_contenu = PATTERN_SIMCARD.sub(remplacer, contenu)

    if nb_modifs == 0:
        return 0

    with open(chemin + ".bak_synctitles", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return nb_modifs


def main():
    fichiers = sorted(glob.glob("article-*.html"))
    print(f"Construction du dictionnaire de titres ({len(fichiers)} fichiers)...")
    titres = construire_dictionnaire_titres(fichiers)
    print(f"Dictionnaire construit : {len(titres)} titres trouvés.\n")

    total_fichiers_modifies = 0
    total_remplacements = 0

    for fichier in fichiers:
        nb = traiter_fichier(fichier, titres)
        if nb > 0:
            total_fichiers_modifies += 1
            total_remplacements += nb

    print(f"=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers_modifies}")
    print(f"Liens croisés corrigés : {total_remplacements}")


if __name__ == "__main__":
    main()
