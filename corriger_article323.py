#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réécriture article-323.html — distinction combles perdus / aménagés MaPrimeRénov'
À lancer depuis ~/Desktop/mon site

Changement de fond depuis le 1er janvier 2026 (sources convergentes,
notamment Hellowatt, Quelle Énergie) : les COMBLES PERDUS ne sont plus
éligibles à MaPrimeRénov' en parcours "par geste" — seuls les RAMPANTS
DE TOITURE et COMBLES AMÉNAGÉS le restent (forfait jusqu'à 75€/m² pour
les revenus très modestes). L'opération "Isolation à 1€" reposait sur
la combinaison MaPrimeRénov' + CEE pour les combles perdus : ce
mécanisme n'est plus garanti tel que décrit depuis 2026.

Modifications :
1. Dates 2025 -> 2026
2. Carte MaPrimeRénov' : précise qu'elle s'applique aux rampants/combles
   aménagés, pas aux combles perdus
3. Carte CEE : retire l'affirmation ferme sur le "1€" pour combles perdus
4. Encart "Isolation à 1€" : reformulé avec la nuance nécessaire (CEE
   seul reste possible pour combles perdus, MaPrimeRénov' non garanti)

Idempotent. Sauvegarde en .bak_art323.

Usage :
    python3 corriger_article323.py
"""

import os

FICHIER = "article-323.html"

REMPLACEMENTS = [
    (
        '<meta name="description" content="Isolation des combles : coût et subventions — Isolation à 1€ possible. Guide complet sur Economya.fr">',
        '<meta name="description" content="Isolation des combles : coût et subventions 2026 — aides selon le type de combles. Guide complet sur Economya.fr">',
    ),
    (
        '<div class="savings-badge">💰 Isolation à 1 € possible</div>',
        '<div class="savings-badge">💰 Aides selon le type de combles</div>',
    ),
    (
        "💶 Les aides disponibles en 2025",
        "💶 Les aides disponibles en 2026",
    ),
    (
        "Aide principale de l'État. Montant selon revenus et nature des travaux. Pour les ménages très modestes, peut couvrir 75 à 90 % du coût de l'isolation des combles. Demande sur maprimerenov.gouv.fr avant travaux.",
        "Aide principale de l'État. ⚠️ Depuis le 1er janvier 2026, seuls les rampants de toiture et combles aménagés restent éligibles au parcours \"par geste\" (jusqu'à 75€/m² pour les revenus très modestes) — les combles perdus en sont exclus et nécessitent désormais une rénovation d'ampleur. Demande sur maprimerenov.gouv.fr avant travaux.",
    ),
    (
        "Prime versée par les fournisseurs d'énergie. Cumulable avec MaPrimeRénov'. Pour les ménages modestes isolant des combles perdus, la combinaison MPR + CEE peut ramener le reste à charge à 1 €.",
        "Prime versée par les fournisseurs d'énergie, cumulable avec MaPrimeRénov' pour les rampants/combles aménagés. Pour les combles perdus (non éligibles à MPR depuis 2026), les CEE seuls peuvent encore couvrir une large partie du coût selon le fournisseur — vérifiez les offres actuelles avant de vous engager.",
    ),
    (
        '<strong>💡 L\'isolation à 1 € : pour qui et comment ?</strong>\n    L\'opération "Isolation à 1 €" (officiellement "Coup de Pouce CEE") est réservée aux ménages modestes et très modestes (revenus sous les plafonds ANAH). En combinant MaPrimeRénov\' + CEE Coup de Pouce, le reste à charge peut effectivement descendre à 1 € symbolique pour les combles perdus. Vérifiez votre éligibilité sur faire.fr.',
        '<strong>💡 L\'isolation à 1 € : ce qui a changé en 2026</strong>\n    L\'opération "Isolation à 1 €" reposait jusqu\'ici sur la combinaison MaPrimeRénov\' + CEE pour les combles perdus. Depuis le 1er janvier 2026, MaPrimeRénov\' ne finance plus les combles perdus en parcours simple — ce mécanisme à 1€ symbolique n\'est donc plus garanti tel que décrit. Certaines offres CEE seules (Coup de Pouce) peuvent encore proposer un reste à charge très faible selon le fournisseur et votre éligibilité, mais vérifiez précisément les conditions actuelles avant de signer quoi que ce soit — et restez prudent face aux démarchages promettant encore "l\'isolation à 1€" sans nuance.',
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

    with open(FICHIER + ".bak_art323", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   Distinction combles perdus (exclus MPR) vs aménagés (éligibles)")
    print("   Nuance ajoutée sur le mécanisme 'isolation à 1€'")


if __name__ == "__main__":
    main()
