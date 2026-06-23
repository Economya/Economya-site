#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des formulations de légalité absolue — partenaire Sharesub
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Problème : "Partagez vos abonnements légalement avec Sharesub" et
"vous divisez la facture par 4 légalement" présentent le partage
d'abonnement comme universellement légal. C'est vrai pour Spotify Famille,
Apple Music, Microsoft 365 — mais Netflix et Disney+ interdisent
explicitement le partage hors foyer dans leurs CGU. La formulation est
donc trompeuse sans nuance.

Corrections :
1. Titre du bloc partenaire (6 articles) : "légalement" -> "en toute sécurité"
2. Phrase article-13.html : ajoute la nuance sur les CGU

Idempotent. Sauvegarde en .bak_sharesub avant modification.

Usage :
    python3 corriger_sharesub.py
"""

import os

FICHIERS_BLOC = [
    "article-141.html",
    "article-143.html",
    "article-188.html",
    "article-250.html",
    "article-502.html",
    "article-504.html",
]

ANCIEN_TITRE = "Partagez vos abonnements légalement avec Sharesub"
NOUVEAU_TITRE = "Partagez vos abonnements en toute sécurité avec Sharesub"

ANCIENNE_PHRASE_13 = "En partageant avec 3 ou 4 personnes via des plateformes comme Sharesub, vous divisez la facture par 4 légalement."
NOUVELLE_PHRASE_13 = "En partageant avec 3 ou 4 personnes via des plateformes comme Sharesub, vous divisez la facture par 4. Vérifiez les conditions d'utilisation du service concerné : certains (Spotify Famille, Apple Music) autorisent le partage, d'autres (Netflix, Disney+) l'interdisent hors foyer."


def corriger_bloc(chemin):
    if not os.path.exists(chemin):
        return "introuvable"
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVEAU_TITRE in contenu:
        return "déjà corrigé"
    if ANCIEN_TITRE not in contenu:
        return "texte attendu absent"
    with open(chemin + ".bak_sharesub", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau = contenu.replace(ANCIEN_TITRE, NOUVEAU_TITRE)
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    return "corrigé"


def corriger_article13(chemin="article-13.html"):
    if not os.path.exists(chemin):
        return "introuvable"
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if NOUVELLE_PHRASE_13 in contenu:
        return "déjà corrigé"
    if ANCIENNE_PHRASE_13 not in contenu:
        return "texte attendu absent"
    with open(chemin + ".bak_sharesub", 'w', encoding='utf-8') as f:
        f.write(contenu)
    nouveau = contenu.replace(ANCIENNE_PHRASE_13, NOUVELLE_PHRASE_13)
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    return "corrigé"


def main():
    print("=== Blocs partenaires (titre) ===")
    for fichier in FICHIERS_BLOC:
        statut = corriger_bloc(fichier)
        print(f"{fichier} : {statut}")

    print("\n=== article-13.html (phrase contextuelle) ===")
    statut13 = corriger_article13()
    print(f"article-13.html : {statut13}")


if __name__ == "__main__":
    main()
