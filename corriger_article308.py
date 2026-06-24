#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-308.html — PreParE obsolète + erreur conceptuelle
À lancer depuis ~/Desktop/mon site

Corrections vérifiées (revalorisation 1er avril 2026, sources convergentes
CAF/Service-Public) :
1. Badge "Jusqu'à 600€/mois" -> "Jusqu'à 459€/mois" (le montant de 600€ était
   déjà faux avant même l'obsolescence — aucun taux PreParE n'atteint 600€)
2. PreParE taux plein : 432€ -> 459,70€
3. PreParE taux partiel mi-temps : 278€ -> 297,17€
4. PreParE majorée : 596€ -> 751,40€
5. ⚠️ ERREUR DE FOND CORRIGÉE : la "PreParE majorée" ne s'applique PAS "si les
   deux parents l'utilisent" (ça n'augmente pas le montant, juste la durée
   plafonnée). La vraie majoration s'applique aux familles de 3 enfants ou
   plus en cessation totale d'activité, sur une durée plus courte (8 mois
   max par parent). Le texte explicatif a été corrigé en conséquence.

Idempotent. Sauvegarde en .bak_art308.

Usage :
    python3 corriger_article308.py
"""

import os

FICHIER = "article-308.html"

REMPLACEMENTS = [
    (
        "Congé parental : droits et allocations — PreParE jusqu'à 600€/mois. Guide complet sur Economya.fr",
        "Congé parental : droits et allocations — PreParE jusqu'à 459€/mois. Guide complet sur Economya.fr",
    ),
    (
        "💰 PreParE jusqu'à 600 €/mois",
        "💰 PreParE jusqu'à 459 €/mois",
    ),
    (
        "📅 Vérifié mai 2025",
        "📅 Vérifié juin 2026",
    ),
    (
        "Le congé parental permet à l'un des parents de cesser ou réduire son activité professionnelle après la naissance d'un enfant, tout en percevant la PreParE (Prestation Partagée d'Éducation de l'Enfant). Un dispositif sous-utilisé qui peut représenter jusqu'à 600 € par mois pendant 6 mois.",
        "Le congé parental permet à l'un des parents de cesser ou réduire son activité professionnelle après la naissance d'un enfant, tout en percevant la PreParE (Prestation Partagée d'Éducation de l'Enfant). Un dispositif sous-utilisé qui peut représenter jusqu'à 459 € par mois pendant 6 mois.",
    ),
    (
        '<span class="opt-amt">432 €/mois</span><span class="opt-sub">PreParE taux plein (2025)</span>',
        '<span class="opt-amt">459,70 €/mois</span><span class="opt-sub">PreParE taux plein (2026)</span>',
    ),
    (
        '<span class="opt-amt">278 €/mois</span><span class="opt-sub">PreParE taux partiel (mi-temps)</span>',
        '<span class="opt-amt">297,17 €/mois</span><span class="opt-sub">PreParE taux partiel (mi-temps, 2026)</span>',
    ),
    (
        "<h3>PreParE majorée (si les deux parents l'utilisent)</h3>",
        "<h3>PreParE majorée (familles de 3 enfants ou plus)</h3>",
    ),
    (
        "Si les deux parents prennent chacun un congé parental, la durée totale est allongée de 6 mois et le montant est légèrement majoré. Le second parent (souvent le père) perçoit la PreParE augmentée.",
        "Réservée aux familles d'au moins 3 enfants en cessation totale d'activité, cette version majorée verse un montant plus élevé, mais sur une durée plus courte (8 mois maximum par parent, jusqu'au 1er anniversaire du plus jeune enfant). Ce choix est définitif et incompatible avec un temps partiel.",
    ),
    (
        '<span class="opt-amt">596 €/mois</span><span class="opt-sub">PreParE majorée 2025</span>',
        '<span class="opt-amt">751,40 €/mois</span><span class="opt-sub">PreParE majorée (2026)</span>',
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

    with open(FICHIER + ".bak_art308", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   (dont la correction de l'erreur conceptuelle sur la PreParE majorée)")


if __name__ == "__main__":
    main()
