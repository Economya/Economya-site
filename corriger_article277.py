#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-277.html — prix Interrail obsolètes + dates
À lancer depuis ~/Desktop/mon site

Confirmé avec forte convergence (Seat61, Eurail.com, plusieurs guides
2026) : le tarif "4 jours/1 mois adulte" est passé de 209€ à 283€ — une
vraie hausse de prix, pas une coquetterie d'arrondi. Jeune (-25%) : 212€.
Senior (-10%) : 255€. Ces 3 chiffres ont une convergence très forte.

⚠️ Pour les autres durées (5j, 7j, 15j, 1 mois), les sources disponibles
divergent légèrement (probablement effet saisonnier) — la ligne 4 jours
est corrigée avec confiance, le reste du tableau reçoit une note
d'avertissement plutôt que des chiffres devinés.

Idempotent. Sauvegarde en .bak_art277.

Usage :
    python3 corriger_article277.py
"""

import os

FICHIER = "article-277.html"

REMPLACEMENTS = [
    (
        "Interrail 2025 : guide complet Europe en train — Europe entière dès 209€. Guide complet sur Economya.fr",
        "Interrail 2026 : guide complet Europe en train — Europe entière dès 283€. Guide complet sur Economya.fr",
    ),
    (
        '"headline": "Interrail 2025 : guide complet Europe en train",',
        '"headline": "Interrail 2026 : guide complet Europe en train",',
    ),
    (
        '<meta property="og:title" content="Interrail 2025 : guide complet Europe en train">',
        '<meta property="og:title" content="Interrail 2026 : guide complet Europe en train">',
    ),
    (
        '<meta name="twitter:title" content="Interrail 2025 : guide complet Europe en train">',
        '<meta name="twitter:title" content="Interrail 2026 : guide complet Europe en train">',
    ),
    (
        "<h1>Interrail 2025 :<br><em>guide complet Europe en train</em></h1>",
        "<h1>Interrail 2026 :<br><em>guide complet Europe en train</em></h1>",
    ),
    (
        '<div class="savings-badge">💰 Europe entière dès 209 €</div>',
        '<div class="savings-badge">💰 Europe entière dès 283 €</div>',
    ),
    (
        "Le pass Interrail permet de voyager en train dans 33 pays européens avec un seul billet. À partir de 209 € pour un adulte, c'est l'une des façons les plus économiques et les plus écologiques de découvrir l'Europe. Voici tout ce qu'il faut savoir pour bien le choisir.",
        "Le pass Interrail permet de voyager en train dans 33 pays européens avec un seul billet. À partir de 283 € pour un adulte, c'est l'une des façons les plus économiques et les plus écologiques de découvrir l'Europe. Voici tout ce qu'il faut savoir pour bien le choisir.",
    ),
    (
        "🎟️ Les différents pass Interrail en 2025",
        "🎟️ Les différents pass Interrail en 2026 — vérifiez les tarifs exacts sur interrail.eu",
    ),
    (
        '<tr><td>Global 4 jours / 1 mois</td><td class="o">209 €</td><td class="g">157 €</td><td class="g">188 €</td></tr>',
        '<tr><td>Global 4 jours / 1 mois</td><td class="o">283 €</td><td class="g">212 €</td><td class="g">255 €</td></tr>',
    ),
]


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    nb_modifs = 0

    for ancien, nouveau in REMPLACEMENTS:
        if nouveau in contenu and ancien not in contenu:
            continue
        if ancien in contenu:
            contenu = contenu.replace(ancien, nouveau)
            nb_modifs += 1

    if nb_modifs == 0:
        print("✅ Déjà corrigé ou textes attendus non trouvés.")
        return

    with open(FICHIER + ".bak_art277", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Prix 4j confirme 209e->283e, dates 2026, autres lignes a verifier")


if __name__ == "__main__":
    main()
