#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction lot 2 — article-430.html et article-437.html
À lancer depuis ~/Desktop/mon site

article-430.html :
1. Tranche d'impôt obsolète : 29 315-83 823€ -> 29 579-84 577€ (barème 2026,
   déjà corrigé ailleurs aujourd'hui, oublié ici)
2. PFU 30% -> 31,4% (dividendes/plus-values, concernés par la hausse)

article-437.html (recalcul complet de l'exemple chiffré) :
1. PFU 30% -> 31,4% sur tout l'article
2. Prélèvements sociaux 17,2% -> 18,6% dans le tableau comparatif
3. Total PFU recalculé : 292€ -> 314€ (1000€ dividendes, TMI 11%)
4. Total barème recalculé : 238€ -> 252€ (PS désormais sur 18,6% aussi)
5. PEA : prélèvements sociaux 17,2% -> 18,6% (le PEA n'est pas exempté de
   la hausse, contrairement à l'assurance-vie)

Idempotent. Sauvegarde en .bak_flattax2.

Usage :
    python3 corriger_flattax_lot2.py
"""

import os

REMPLACEMENTS = {
    "article-430.html": [
        (
            '<tr><td>29 315 à 83 823 €</td><td class="o">30 %</td><td>Tranche "classe moyenne"</td></tr>',
            '<tr><td>29 579 à 84 577 €</td><td class="o">30 %</td><td>Tranche "classe moyenne"</td></tr>',
        ),
        (
            "Le PFU (Prélèvement Forfaitaire Unique) de 30 % s'applique sur les revenus financiers (dividendes, plus-values). Option pour le barème progressif si votre taux marginal est inférieur à 30 % (revenus inférieurs à environ 77 000 €).",
            "Le PFU (Prélèvement Forfaitaire Unique) de 31,4 % (depuis 2026) s'applique sur les revenus financiers (dividendes, plus-values). Option pour le barème progressif si votre taux marginal est inférieur à 30 %.",
        ),
    ],
    "article-437.html": [
        (
            '<span class="comp-h-col">PFU 30 % · Barème progressif</span>',
            '<span class="comp-h-col">PFU 31,4 % · Barème progressif</span>',
        ),
        (
            '<div class="comp-row"><span class="comp-label">Prélèvements sociaux (17,2 %)</span><span class="comp-pfu">172 €</span><span class="comp-bareme">172 €</span></div>',
            '<div class="comp-row"><span class="comp-label">Prélèvements sociaux (18,6 %)</span><span class="comp-pfu">186 €</span><span class="comp-bareme">186 €</span></div>',
        ),
        (
            '<div class="comp-row"><span class="comp-label">Total fiscal</span><span class="comp-pfu" style="font-size:.92rem">292 €</span><span class="comp-bareme" style="font-size:.92rem">238 €</span></div>',
            '<div class="comp-row"><span class="comp-label">Total fiscal</span><span class="comp-pfu" style="font-size:.92rem">314 €</span><span class="comp-bareme" style="font-size:.92rem">252 €</span></div>',
        ),
        (
            "* À TMI 11 % : le barème progressif est plus avantageux (238 vs 292 €). À TMI 30 % et au-delà, la flat tax est généralement plus avantageuse. La CSG de 6,8 % est déductible du revenu au barème (avantage supplémentaire).",
            "* À TMI 11 % : le barème progressif est plus avantageux (252 vs 314 €). À TMI 30 % et au-delà, la flat tax est généralement plus avantageuse. La CSG de 6,8 % est déductible du revenu au barème (avantage supplémentaire).",
        ),
        (
            "Dividendes et plus-values exonérés d'IR après 5 ans. Seuls les prélèvements sociaux (17,2 %) s'appliquent. Plafond 150 000 €. Uniquement actions européennes.",
            "Dividendes et plus-values exonérés d'IR après 5 ans. Seuls les prélèvements sociaux (18,6 % depuis 2026) s'appliquent. Plafond 150 000 €. Uniquement actions européennes.",
        ),
        (
            '<div class="e-fiscalite">PFU 30 % par défaut</div>',
            '<div class="e-fiscalite">PFU 31,4 % par défaut</div>',
        ),
        (
            "Flat tax 30 % sur dividendes et plus-values. Option barème progressif possible si TMI &lt;30 %. Aucune limite de versement, toutes valeurs mondiales.",
            "Flat tax 31,4 % (depuis 2026) sur dividendes et plus-values. Option barème progressif possible si TMI &lt;30 %. Aucune limite de versement, toutes valeurs mondiales.",
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

        with open(fichier + ".bak_flattax2", 'w', encoding='utf-8') as f:
            f.write(contenu_original)

        with open(fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)

        print(f"✅ {fichier} : {nb_modifs_fichier} remplacement(s)")
        total_fichiers += 1
        total_remplacements += nb_modifs_fichier

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fichiers modifiés : {total_fichiers}")
    print(f"Remplacements totaux : {total_remplacements}")


if __name__ == "__main__":
    main()
