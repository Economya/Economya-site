#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction des titres collés (mots accolés sans espace) sur les cartes
de la page d'accueil index.html
À lancer depuis ~/Desktop/mon site

DÉCOUVERTE : 26 titres de cartes ("atitle") sur index.html ont des mots
collés sans espace, probablement causé par la suppression d'un retour
à la ligne lors d'une édition antérieure du fichier source des titres
(ex: "d'intérieursans" au lieu de "d'intérieur sans", "Black Friday
:acheter" au lieu de "Black Friday : acheter"). Confirmé visuellement
par capture d'écran de la page rendue.

Chaque remplacement est fait individuellement (texte exact, pas de
regex générique) pour exclure tout risque de casser un mot légitime
comme "artisans" qui contient lui aussi la suite de lettres "sans".

Idempotent. Sauvegarde en .bak_titrescolles avant modification.

Usage :
    python3 corriger_index_titres_colles.py
"""

import os

FICHIER = "index.html"

REMPLACEMENTS = [
    ("Sortir en famillesans se ruiner : 10 idées", "Sortir en famille sans se ruiner : 10 idées"),
    ("Manger biosans se ruiner", "Manger bio sans se ruiner"),
    ("Rentrée scolairepas chère", "Rentrée scolaire pas chère"),
    ("Vacances en Francepas chères", "Vacances en France pas chères"),
    ("Apprendre un instrumentsans professeur payant", "Apprendre un instrument sans professeur payant"),
    ("Location de voiturepas chère", "Location de voiture pas chère"),
    ("Black Friday :acheter malin ou éviter le piège ?", "Black Friday : acheter malin ou éviter le piège ?"),
    ("Concerts et festivalspas chers", "Concerts et festivals pas chers"),
    ("Arts martiaux et sports de combatpas chers", "Arts martiaux et sports de combat pas chers"),
    ("Fleurs et plantes d'intérieursans se ruiner", "Fleurs et plantes d'intérieur sans se ruiner"),
    ("Sports nautiquespas chers", "Sports nautiques pas chers"),
    ("Faire ses propresproduits ménagers", "Faire ses propres produits ménagers"),
    ("Assurance habitationpas chère", "Assurance habitation pas chère"),
    ("Jardinage et potagerpas cher", "Jardinage et potager pas cher"),
    ("Voyager en trainpas cher</div>", "Voyager en train pas cher</div>"),
    ("Bien vieillirsans se ruiner", "Bien vieillir sans se ruiner"),
    ("Préparer sa retraitesans se tromper", "Préparer sa retraite sans se tromper"),
    ("Anniversaires d'enfantspas chers et réussis", "Anniversaires d'enfants pas chers et réussis"),
    ("Voyager en trainpas cher : maîtriser la SNCF", "Voyager en train pas cher : maîtriser la SNCF"),
    ("Les soldes : acheter malinsans se faire avoir", "Les soldes : acheter malin sans se faire avoir"),
    ("Déménagersans se ruiner", "Déménager sans se ruiner"),
    ("Gérer un budget en couplesans se disputer", "Gérer un budget en couple sans se disputer"),
    ("Plongée sous-marinepas chère", "Plongée sous-marine pas chère"),
    ("Cuisiner pour les intolérantssans se ruiner", "Cuisiner pour les intolérants sans se ruiner"),
    ("Alimentation durablesans se ruiner", "Alimentation durable sans se ruiner"),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return
    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0
    deja_ok = 0

    for ancien, nouveau in REMPLACEMENTS:
        if nouveau in contenu:
            deja_ok += 1
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau, 1)
            nb_modifs += 1
        else:
            print(f"⚠️  Texte non trouvé (ignoré) : {ancien[:60]}...")

    if nb_modifs == 0:
        print(f"✅ Déjà corrigé ({deja_ok}/{len(REMPLACEMENTS)} titres déjà bons).")
        return

    with open(FICHIER + ".bak_titrescolles", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} titre(s) corrigé(s) sur index.html (espaces manquants)")
    if deja_ok:
        print(f"   ({deja_ok} étaient déjà corrects)")


if __name__ == "__main__":
    main()
