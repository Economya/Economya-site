#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-349.html — erreur majeure du tableau fiscal + amende
incorrecte + dates
À lancer depuis ~/Desktop/mon site

ERREUR MAJEURE corrigée : le tableau confondait les seuils "classé" et
"non classé". Les VRAIS seuils 2026 (confirmés par de nombreuses sources
convergentes, loi Le Meur du 19/11/2024) :
- Meublé NON CLASSÉ : plafond 15 000€/an (effondré depuis 77 700€),
  abattement 30% (effondré depuis 50%)
- Meublé CLASSÉ (et chambres d'hôtes) : plafond 77 700€ (2025) / 83 600€
  (2026), abattement 50% (réduit depuis 71%)

Amende corrigée : le dépassement du plafond de jours (120j, ou 90j si la
commune l'a abaissé) expose à une amende de 15 000€ — pas 50 000€ comme
indiqué (ce dernier montant, doublé à 100 000€ en 2026, concerne une
violation différente : le changement d'usage non autorisé).

Idempotent. Sauvegarde en .bak_art349.

Usage :
    python3 corriger_article349.py
"""

import os

FICHIER = "article-349.html"

REMPLACEMENTS = [
    (
        "Location saisonnière : cadre légal 2025 — Évitez les amendes. Guide complet sur Economya.fr",
        "Location saisonnière : cadre légal 2026 — Évitez les amendes. Guide complet sur Economya.fr",
    ),
    (
        "<title>Location saisonnière : cadre légal 2025 — Economya.fr</title>",
        "<title>Location saisonnière : cadre légal 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Location saisonnière : cadre légal 2025",',
        '"headline": "Location saisonnière : cadre légal 2026",',
    ),
    (
        '<meta property="og:title" content="Location saisonnière : cadre légal 2025">',
        '<meta property="og:title" content="Location saisonnière : cadre légal 2026">',
    ),
    (
        '<meta name="twitter:title" content="Location saisonnière : cadre légal 2025">',
        '<meta name="twitter:title" content="Location saisonnière : cadre légal 2026">',
    ),
    (
        "<h1>Location saisonnière :<br><em>cadre légal 2025</em></h1>",
        "<h1>Location saisonnière :<br><em>cadre légal 2026</em></h1>",
    ),
    (
        "Enregistrement obligatoire, quotas de jours, fiscalité alourdie, pouvoirs des maires renforcés : voici ce que tout propriétaire doit savoir en 2025 pour louer en toute légalité.",
        "Enregistrement obligatoire, quotas de jours, fiscalité alourdie, pouvoirs des maires renforcés : voici ce que tout propriétaire doit savoir en 2026 pour louer en toute légalité.",
    ),
    (
        "⚖️ Les règles essentielles en 2025",
        "⚖️ Les règles essentielles en 2026",
    ),
    (
        "La location de votre résidence principale sur des plateformes comme Airbnb est légalement limitée à 120 jours par an. Airbnb bloque automatiquement votre calendrier après 120 nuits. Au-delà, c'est illégal et les amendes peuvent atteindre 50 000 €.",
        "La location de votre résidence principale sur des plateformes comme Airbnb est légalement limitée à 120 jours par an (certaines communes peuvent abaisser ce seuil à 90 jours par délibération du conseil municipal). Airbnb bloque automatiquement votre calendrier après 120 nuits. Au-delà, c'est illégal et l'amende civile peut atteindre 15 000 €.",
    ),
    (
        "✅ DPE obligatoire dès 2025 puis 2034",
        "✅ DPE obligatoire dès 2026 puis 2034",
    ),
    (
        "💰 La fiscalité des revenus de location courte durée en 2025",
        "💰 La fiscalité des revenus de location courte durée en 2026",
    ),
    (
        '<tr><td>Micro-BIC meublé classique</td><td class="o">&lt; 77 700 €/an</td><td class="g">50 % d\'abattement</td><td>50 % imposés à l\'IR + PS</td></tr>\n        <tr><td>Micro-BIC meublé classé ★ (loi 2024)</td><td class="o">&lt; 77 700 €/an</td><td class="g">50 % d\'abattement (abaissé de 71 % en 2023)</td><td>50 % imposés à l\'IR + PS</td></tr>\n        <tr><td>Meublé de tourisme classé (zone tendue)</td><td class="r">Abattement réduit depuis 2024</td><td class="r">50 % (vs 71 % avant)</td><td>Plus d\'avantage spécial</td></tr>',
        '<tr><td>Micro-BIC meublé NON classé</td><td class="r">&lt; 15 000 €/an</td><td class="r">30 % d\'abattement (effondré depuis 50 % avant la loi Le Meur)</td><td>70 % imposés à l\'IR + PS</td></tr>\n        <tr><td>Micro-BIC meublé CLASSÉ ★ (loi Le Meur)</td><td class="o">&lt; 77 700 €/an (83 600 € pour les revenus 2026)</td><td class="g">50 % d\'abattement (réduit depuis 71 % avant la loi)</td><td>50 % imposés à l\'IR + PS</td></tr>\n        <tr><td>⚠️ Au-delà des plafonds ci-dessus</td><td class="r">Passage obligatoire au régime réel</td><td class="r">Charges et amortissements réels déductibles</td><td>Peut être plus avantageux selon les charges</td></tr>',
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

    with open(FICHIER + ".bak_art349", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   ERREUR MAJEURE corrigee: tableau classe/non-classe refait,")
    print("   amende 50000e->15000e (bonne violation), dates 2026")


if __name__ == "__main__":
    main()
