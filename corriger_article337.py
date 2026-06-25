#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-337.html — taux des livrets réglementés obsolètes
À lancer depuis ~/Desktop/mon site

Taux confirmés depuis le 1er février 2026 (sources officielles
convergentes : economie.gouv.fr, service-public.gouv.fr, Banque de
France, ABE Infoservice) :
- Livret A : 2,4% -> 1,5% (était 1,7% avant le 01/02/2026)
- LEP : 4,0% -> 2,5% (était 2,7% avant le 01/02/2026)
- LDDS : 2,4% -> 1,5% (toujours identique au Livret A)
- CEL : 2% -> 1% (= 2/3 du taux Livret A)
- PEL : 2,25% garanti -> précision sur 2024 vs nouveau taux 2026 (2%)

Cascade recalculée : écart LEP/Livret A = 2,5-1,5 = 1,0 point (au lieu de
1,6%) ; sur 10 000€, 100€ supplémentaires/an (au lieu de 160€).

Idempotent. Sauvegarde en .bak_art337.

Usage :
    python3 corriger_article337.py
"""

import os

FICHIER = "article-337.html"

REMPLACEMENTS = [
    (
        "Livret A vs LEP vs LDDS : que choisir en 2025 — LEP à 4% : ouvrez-le. Guide complet sur Economya.fr",
        "Livret A vs LEP vs LDDS : que choisir en 2026 — LEP à 2,5% : ouvrez-le. Guide complet sur Economya.fr",
    ),
    (
        "<title>Livret A vs LEP vs LDDS : que choisir en 2025 — Economya.fr</title>",
        "<title>Livret A vs LEP vs LDDS : que choisir en 2026 — Economya.fr</title>",
    ),
    (
        '"headline": "Livret A vs LEP vs LDDS : que choisir en 2025",',
        '"headline": "Livret A vs LEP vs LDDS : que choisir en 2026",',
    ),
    (
        '<meta property="og:title" content="Livret A vs LEP vs LDDS : que choisir en 2025">',
        '<meta property="og:title" content="Livret A vs LEP vs LDDS : que choisir en 2026">',
    ),
    (
        '<meta name="twitter:title" content="Livret A vs LEP vs LDDS : que choisir en 2025">',
        '<meta name="twitter:title" content="Livret A vs LEP vs LDDS : que choisir en 2026">',
    ),
    (
        "<h1>Livret A vs LEP vs LDDS :<br><em>que choisir en 2025</em></h1>",
        "<h1>Livret A vs LEP vs LDDS :<br><em>que choisir en 2026</em></h1>",
    ),
    (
        '<div class="savings-badge">💰 LEP à 4 % : ouvrez-le</div>',
        '<div class="savings-badge">💰 LEP à 2,5 % : ouvrez-le</div>',
    ),
    (
        "Livret A, LEP, LDDS, CEL — tous ces livrets réglementés sont sécurisés et défiscalisés. Mais leurs taux et conditions varient fortement. En 2025, le LEP à 4 % est de loin le meilleur placement sans risque en France pour ceux qui y sont éligibles. Comparatif complet.",
        "Livret A, LEP, LDDS, CEL — tous ces livrets réglementés sont sécurisés et défiscalisés. Mais leurs taux et conditions varient fortement. Depuis février 2026, le LEP à 2,5 % est de loin le meilleur placement sans risque en France pour ceux qui y sont éligibles. Comparatif complet.",
    ),
    (
        '<span class="star-badge">⭐ Meilleur taux 2025</span>',
        '<span class="star-badge">⭐ Meilleur taux 2026</span>',
    ),
    (
        '<span class="l-taux">4,0 %</span>',
        '<span class="l-taux">2,5 %</span>',
    ),
    (
        '<span class="l-taux">2,4 %</span>',
        '<span class="l-taux">1,5 %</span>',
    ),
    (
        '<span class="l-taux">2 %</span>',
        '<span class="l-taux">1 %</span>',
    ),
    (
        '⚠️ Taux brut soumis à la flat tax (2 % × 0,7 = 1,4 % net réel). Moins intéressant que les autres livrets sauf si vous visez un prêt immobilier à taux réduit associé.',
        '⚠️ Taux brut soumis à la flat tax (1 % × 0,686 ≈ 0,7 % net réel). Moins intéressant que les autres livrets sauf si vous visez un prêt immobilier à taux réduit associé.',
    ),
    (
        '<tr><td>Projet immobilier dans 4+ ans</td><td class="o">PEL (2,25 % garanti) + CEL pour les droits à prêt</td></tr>',
        '<tr><td>Projet immobilier dans 4+ ans</td><td class="o">PEL (2 % pour les nouvelles ouvertures en 2026 ; les PEL ouverts avant gardent leur taux d\'origine) + CEL pour les droits à prêt</td></tr>',
    ),
    (
        "💡 Vérifiez votre éligibilité au LEP — beaucoup ratent 1,6 % de rendement",
        "💡 Vérifiez votre éligibilité au LEP — beaucoup ratent 1 point de rendement",
    ),
    (
        'Environ 18 millions de Français sont éligibles au LEP mais seulement 10 millions l\'ont ouvert. Avec un écart de 1,6 % vs le Livret A, sur 10 000 € c\'est 160 € d\'intérêts supplémentaires par an pour rien. Vérifiez sur votre espace impots.gouv.fr (rubrique "Accès livret d\'épargne populaire").',
        'Environ 18 millions de Français sont éligibles au LEP mais seulement 10 millions l\'ont ouvert. Avec un écart de 1 point vs le Livret A, sur 10 000 € c\'est 100 € d\'intérêts supplémentaires par an pour rien. Vérifiez sur votre espace impots.gouv.fr (rubrique "Accès livret d\'épargne populaire").',
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

    with open(FICHIER + ".bak_art337", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Taux livrets 2026: LEP 2,5%, Livret A/LDDS 1,5%, CEL 1%")


if __name__ == "__main__":
    main()
