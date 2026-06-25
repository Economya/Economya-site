#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-349.html (2e passage) — tableau fiscal ligne par ligne
+ note de bas de tableau
À lancer depuis ~/Desktop/mon site

Le 1er script avait un bloc combiné trop spécifique qui ne correspondait
pas à la structure réelle (une ligne "Régime réel BIC" intercalée cassait
le motif). Cette fois, chaque ligne est corrigée individuellement.

Idempotent. Sauvegarde en .bak_art349v2.

Usage :
    python3 corriger_article349_v2.py
"""

import os

FICHIER = "article-349.html"

REMPLACEMENTS = [
    (
        '<tr><td>Micro-BIC meublé classique</td><td class="o">&lt; 77 700 €/an</td><td class="g">50 % d\'abattement</td><td>50 % imposés à l\'IR + PS</td></tr>',
        '<tr><td>Micro-BIC meublé NON classé</td><td class="r">&lt; 15 000 €/an</td><td class="r">30 % d\'abattement (effondré depuis 50 % avant la loi Le Meur)</td><td>70 % imposés à l\'IR + PS</td></tr>',
    ),
    (
        '<tr><td>Micro-BIC meublé classé ★ (loi 2024)</td><td class="o">&lt; 77 700 €/an</td><td class="g">50 % d\'abattement (abaissé de 71 % en 2023)</td><td>50 % imposés à l\'IR + PS</td></tr>',
        '<tr><td>Micro-BIC meublé CLASSÉ ★</td><td class="o">&lt; 77 700 €/an (83 600 € pour les revenus 2026)</td><td class="g">50 % d\'abattement (réduit depuis 71 % avant la loi Le Meur)</td><td>50 % imposés à l\'IR + PS</td></tr>',
    ),
    (
        '<tr><td>Meublé de tourisme classé (zone tendue)</td><td class="r">Abattement réduit depuis 2024</td><td class="r">50 % (vs 71 % avant)</td><td>Plus d\'avantage spécial</td></tr>',
        '<tr><td>Au-delà des plafonds ci-dessus</td><td class="r">Passage obligatoire au régime réel</td><td class="r">Charges et amortissements réels</td><td>Peut être plus avantageux</td></tr>',
    ),
    (
        "* La loi de finances 2024 a supprimé l'abattement de 71 % pour les meublés de tourisme classés. L'abattement est désormais de 50 % pour tous (hors zones tendues où il peut être réduit).",
        "* La loi Le Meur (19/11/2024) a durci la fiscalité : les meublés NON classés voient leur abattement chuter de 50 % à 30 % et leur plafond de 77 700 € à 15 000 €. Les meublés CLASSÉS gardent un régime plus favorable (50 % d'abattement, contre 71 % auparavant). Le classement (1 à 5 étoiles, via un organisme accrédité Atout France) est donc devenu quasi indispensable pour conserver une fiscalité avantageuse.",
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

    with open(FICHIER + ".bak_art349v2", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Tableau fiscal corrige ligne par ligne, note de bas corrigee")


if __name__ == "__main__":
    main()
