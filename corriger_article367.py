#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction article-367.html — montants RSA obsolètes
À lancer depuis ~/Desktop/mon site

Montants vérifiés via sources convergentes (CAF, Service-Public),
revalorisation du 1er avril 2026 :
- Personne seule : 651,69 € (au lieu de 635,71 €)
- Couple sans enfant : 977,54 € (au lieu de 953,57 €)

⚠️ Les lignes "Parent isolé +1 enfant" et "Couple +2 enfants" n'ont PAS été
modifiées — leurs formules exactes (majoration isolement, coefficients par
personne à charge) n'ont pas pu être vérifiées avec une confiance
suffisante. À vérifier manuellement sur caf.fr ou service-public.fr.

Idempotent. Sauvegarde en .bak_art367.

Usage :
    python3 corriger_article367.py
"""

import os

FICHIER = "article-367.html"

REMPLACEMENTS = [
    (
        "RSA : conditions et démarches en 2025 — Jusqu'à 635€/mois. Guide complet sur Economya.fr",
        "RSA : conditions et démarches en 2026 — Jusqu'à 651€/mois. Guide complet sur Economya.fr",
    ),
    (
        "RSA : conditions et démarches en 2025 — Economya.fr",
        "RSA : conditions et démarches en 2026 — Economya.fr",
    ),
    (
        "RSA : conditions et démarches en 2025",  # headline JSON-LD + h1 (deux occurrences identiques)
        "RSA : conditions et démarches en 2026",
    ),
    (
        "<h1>RSA :<br><em>conditions et démarches en 2025</em></h1>",
        "<h1>RSA :<br><em>conditions et démarches en 2026</em></h1>",
    ),
    (
        "💰 Jusqu'à 635 €/mois",
        "💰 Jusqu'à 651 €/mois",
    ),
    (
        "Le RSA (Revenu de Solidarité Active) garantit un revenu minimum aux personnes sans ressources ou aux revenus très faibles. En 2025, le montant de base est de 635,71 € pour une personne seule. Souvent méconnu ou mal compris, le RSA est une aide accessible — voici comment en bénéficier.",
        "Le RSA (Revenu de Solidarité Active) garantit un revenu minimum aux personnes sans ressources ou aux revenus très faibles. En 2026, le montant de base est de 651,69 € pour une personne seule. Souvent méconnu ou mal compris, le RSA est une aide accessible — voici comment en bénéficier.",
    ),
    (
        "💶 Les montants du RSA en 2025",
        "💶 Les montants du RSA en 2026",
    ),
    (
        '<div class="m-amount">635,71 €</div>',
        '<div class="m-amount">651,69 €</div>',
    ),
    (
        "Montant de base mensuel net 2025",
        "Montant de base mensuel net 2026",
    ),
    (
        '<div class="m-amount">953,57 €</div>',
        '<div class="m-amount">977,54 €</div>',
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

    with open(FICHIER + ".bak_art367", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ {nb_modifs} remplacement(s) appliqué(s) sur {FICHIER}")
    print("   ⚠️  Lignes 'Parent isolé +1 enfant' et 'Couple +2 enfants' NON vérifiées")
    print("      — à contrôler manuellement sur caf.fr")


if __name__ == "__main__":
    main()
