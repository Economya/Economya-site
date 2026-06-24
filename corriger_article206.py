#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réécriture article-206.html — panorama des aides à la rénovation énergétique
À lancer depuis ~/Desktop/mon site

Corrections (sources officielles convergentes 2026) :
1. "Jusqu'à 90% des travaux" -> obsolète (taux maximum réel 2026 : 80%,
   le 90% datait d'avant juin 2025)
2. Description MPR : ajoute la nuance "isolation des murs" et "chaudière
   biomasse" exclues du parcours par geste depuis le 1er janvier 2026
3. Table "Isolation murs ext." : ce parcours simple au m² n'existe plus
   pour ce type de travaux — remplacée par une note explicative
4. Table "Pompe à chaleur" : montants corrigés (5 000/4 000/3 000€ pour
   PAC air/eau, profil rose non éligible au parcours par geste)
5. Dates 2025 -> 2026

Idempotent. Sauvegarde en .bak_art206.

Usage :
    python3 corriger_article206.py
"""

import os

FICHIER = "article-206.html"

REMPLACEMENTS = [
    (
        "Rénovation énergétique : toutes les aides 2025 — Jusqu'à 90% des travaux financés. Guide complet sur Economya.fr",
        "Rénovation énergétique : toutes les aides 2026 — Jusqu'à 80% des travaux financés. Guide complet sur Economya.fr",
    ),
    (
        "Rénovation énergétique : toutes les aides 2025 — Economya.fr",
        "Rénovation énergétique : toutes les aides 2026 — Economya.fr",
    ),
    (
        '"headline": "Rénovation énergétique : toutes les aides 2025",',
        '"headline": "Rénovation énergétique : toutes les aides 2026",',
    ),
    (
        "<h1>Rénovation énergétique : toutes les aides 2025</h1>",
        "<h1>Rénovation énergétique : toutes les aides 2026</h1>",
    ),
    (
        '<meta property="og:title" content="Rénovation énergétique : toutes les aides 2025">',
        '<meta property="og:title" content="Rénovation énergétique : toutes les aides 2026">',
    ),
    (
        '<meta name="twitter:title" content="Rénovation énergétique : toutes les aides 2025">',
        '<meta name="twitter:title" content="Rénovation énergétique : toutes les aides 2026">',
    ),
    (
        "💰 Jusqu'à 90 % des travaux financés",
        "💰 Jusqu'à 80 % des travaux financés",
    ),
    (
        "En 2025, rénover son logement pour réduire sa facture énergétique n'a jamais été aussi bien soutenu par l'État. MaPrimeRénov', les Certificats d'Économies d'Énergie, l'éco-PTZ, la TVA à 5,5 % — l'empilement des aides peut couvrir la quasi-totalité des travaux pour les ménages modestes. Mais le système est complexe, les plafonds varient selon les revenus et les types de travaux, et de nombreuses arnaques circulent. Voici le panorama complet et actualisé des aides disponibles en 2025, avec les montants réels et les conditions d'accès.",
        "En 2026, rénover son logement pour réduire sa facture énergétique reste bien soutenu par l'État, mais le système a changé : MaPrimeRénov' distingue désormais deux parcours (\"par geste\" pour un seul équipement, \"rénovation d'ampleur\" pour un projet plus large), avec des règles d'éligibilité différentes selon le type de travaux. Les CEE, l'éco-PTZ et la TVA à 5,5 % restent cumulables. Voici le panorama complet et actualisé des aides disponibles en 2026, avec les montants réels et les conditions d'accès.",
    ),
    (
        "<span class=\"aide-montant\">Jusqu'à 90 % des travaux</span>",
        "<span class=\"aide-montant\">Jusqu'à 80 % des travaux</span>",
    ),
    (
        "L'aide phare de l'État, versée par l'ANAH. Son montant dépend de vos revenus (4 catégories : bleu, jaune, violet, rose) et du type de travaux. Elle couvre isolation, pompe à chaleur, chaudière biomasse, fenêtres, ventilation. En 2025, elle est accessible aux propriétaires occupants ET aux bailleurs (avec obligation de louer 6 ans après travaux).",
        "L'aide phare de l'État, versée par l'ANAH. Son montant dépend de vos revenus (4 catégories : bleu, jaune, violet, rose) et du type de travaux. ⚠️ Depuis le 1er janvier 2026, l'isolation des murs et les chaudières biomasse ne sont plus finançables via le parcours \"par geste\" — elles nécessitent désormais une rénovation d'ampleur (au moins 2 gestes d'isolation). Pompe à chaleur, fenêtres et ventilation restent éligibles au parcours simple. Accessible aux propriétaires occupants ET aux bailleurs (avec obligation de louer 6 ans après travaux).",
    ),
    (
        '<h2>Montants MaPrimeRénov\' selon revenus — isolation des murs</h2>\n\n  <table class="tableau">\n    <thead><tr><th>Profil de revenus</th><th>Couleur MPR</th><th>Isolation murs ext.</th><th>Pompe à chaleur</th></tr></thead>\n    <tbody>\n      <tr><td>Très modeste</td><td>🔵 Bleu</td><td class="haut">75 €/m²</td><td class="haut">8 000 €</td></tr>\n      <tr><td>Modeste</td><td>🟡 Jaune</td><td class="moyen">60 €/m²</td><td class="moyen">6 000 €</td></tr>\n      <tr><td>Intermédiaire</td><td>🟣 Violet</td><td class="standard">40 €/m²</td><td class="standard">4 000 €</td></tr>\n      <tr><td>Supérieur</td><td>🌸 Rose</td><td class="standard">15 €/m²</td><td class="standard">2 000 €</td></tr>\n    </tbody>\n  </table>',
        '<h2>Montants MaPrimeRénov\' selon revenus — pompe à chaleur (PAC air/eau)</h2>\n\n  <p style="font-size:.85rem;color:var(--m);margin-bottom:1rem">⚠️ L\'isolation des murs n\'a plus de forfait au m² en parcours simple depuis 2026 : elle se finance uniquement via une rénovation d\'ampleur, avec un taux de prise en charge de 45 à 80 % du coût global selon vos revenus (demande accompagnement obligatoire).</p>\n\n  <table class="tableau">\n    <thead><tr><th>Profil de revenus</th><th>Couleur MPR</th><th>Pompe à chaleur air/eau</th></tr></thead>\n    <tbody>\n      <tr><td>Très modeste</td><td>🔵 Bleu</td><td class="haut">5 000 €</td></tr>\n      <tr><td>Modeste</td><td>🟡 Jaune</td><td class="moyen">4 000 €</td></tr>\n      <tr><td>Intermédiaire</td><td>🟣 Violet</td><td class="standard">3 000 €</td></tr>\n      <tr><td>Supérieur</td><td>🌸 Rose</td><td class="standard">Non éligible au parcours simple</td></tr>\n    </tbody>\n  </table>',
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

    with open(FICHIER + ".bak_art206", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Taux 90%->80%, exclusion isolation murs/chaudière biomasse,")
    print("   table PAC corrigée (5000/4000/3000€), dates 2026")


if __name__ == "__main__":
    main()
