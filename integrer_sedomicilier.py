#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du partenaire d'affiliation SeDomicilier (domiciliation
d'entreprise) sur 10 articles ciblés liés à la création d'entreprise /
auto-entrepreneuriat / freelance
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Lien Awin vérifié : awinmid=24149, awinaffid=2926395
Tarif vérifié (juin 2026, sources convergentes) : dès 11€HT/mois pour les
micro-entrepreneurs (engagement 3 ans) ou 16€HT/mois sans engagement,
sans caution ni frais cachés.

Insertion juste avant <footer>, ancrage fiable présent sur toutes les
pages du site.

Idempotent. Sauvegarde en .bak_sedomicilier avant modification.

Usage :
    python3 integrer_sedomicilier.py
"""

import os

FICHIERS_CIBLES = [
    "article-442.html",  # Auto-entrepreneur : charges, cotisations
    "article-443.html",  # Financer sa création d'entreprise à 0€
    "article-484.html",  # ACRE
    "article-489.html",  # BPI France : aides aux entrepreneurs
    "article-467.html",  # Micro-BIC vs BNC
    "article-181.html",  # Freelance : gérer son argent
    "article-420.html",  # Fiverr et Malt
    "article-491.html",  # Freelance et revenus complémentaires
    "article-424.html",  # Newsletter payante
    "article-417.html",  # Tutorat en ligne
]

LIEN_AWIN = "https://www.awin1.com/cread.php?awinmid=24149&awinaffid=2926395&ued=https%3A%2F%2Fsedomicilier.fr"

BLOC_SEDOMICILIER = f'''
  <div class="tip" style="background:#FAEEDA;border-left:4px solid #EF9F27;color:#633806">
    <strong>🏢 Besoin d'une adresse professionnelle pour votre entreprise ?</strong>
    Si vous ne souhaitez pas domicilier votre activité à votre domicile personnel, des services comme <a href="{LIEN_AWIN}" target="_blank" rel="noopener sponsored">SeDomicilier</a> proposent une adresse de siège social dès 11€HT/mois (engagement long terme) ou 16€HT/mois sans engagement, sans caution ni frais cachés, avec gestion du courrier incluse. Cela permet de séparer clairement votre adresse personnelle de votre activité professionnelle. Economya peut percevoir une commission sur ce lien, sans coût supplémentaire pour vous.
  </div>
'''


def traiter_fichier(chemin):
    if not os.path.exists(chemin):
        return "introuvable"

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "SeDomicilier" in contenu:
        return "déjà présent"

    if "<footer>" not in contenu:
        return "pas de footer trouvé"

    contenu_original = contenu
    nouveau_contenu = contenu.replace("<footer>", BLOC_SEDOMICILIER + "\n<footer>", 1)

    with open(chemin + ".bak_sedomicilier", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return "ajouté"


def main():
    resultats = {}
    for fichier in FICHIERS_CIBLES:
        statut = traiter_fichier(fichier)
        resultats[statut] = resultats.get(statut, 0) + 1
        print(f"{fichier} : {statut}")

    print(f"\n=== RÉSUMÉ ===")
    for statut, count in resultats.items():
        print(f"{statut} : {count}")


if __name__ == "__main__":
    main()
