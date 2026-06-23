#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction de l'identité de l'éditeur dans mentions-legales.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Remplace "L'équipe Economya" par le nom complet de l'éditeur (Alexandre Goffinet)
et ajoute une clause justifiant l'absence d'adresse postale publique.

Sans danger à relancer (idempotent). Sauvegarde en .bak_mentions avant modification.

Usage :
    python3 corriger_mentions_legales.py
"""

import os

FICHIER = "mentions-legales.html"

ANCIEN_BLOC = '''  <h2>1. Éditeur du site</h2>
  <p>Le site <strong>Economya.fr</strong> est édité à titre personnel par :</p>
  <p><strong>L'équipe Economya</strong><br>
  Email : <a href="mailto:contact@economya.fr">contact@economya.fr</a></p>'''

NOUVEAU_BLOC = '''  <h2>1. Éditeur du site</h2>
  <p>Le site <strong>Economya.fr</strong> est édité à titre personnel par :</p>
  <p><strong>Alexandre Goffinet</strong><br>
  Email : <a href="mailto:contact@economya.fr">contact@economya.fr</a></p>
  <p style="font-size:.85rem;color:var(--m)">
  Conformément à l'article 6-III de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, l'adresse complète de l'éditeur est tenue à la disposition des autorités compétentes sur simple demande, et n'est pas publiée sur ce site afin de protéger la vie privée de l'éditeur, conformément à la possibilité offerte aux personnes physiques n'agissant pas à titre commercial.
  </p>'''


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable dans ce dossier.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "Alexandre Goffinet" in contenu:
        print("✅ Déjà corrigé — aucune modification nécessaire.")
        return

    if ANCIEN_BLOC not in contenu:
        print("⚠️  Le bloc attendu n'a pas été trouvé tel quel dans le fichier.")
        print("   Aucune modification effectuée, pour éviter une erreur.")
        print("   Vérifie manuellement le contenu actuel du fichier.")
        return

    # Sauvegarde
    with open(FICHIER + ".bak_mentions", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(ANCIEN_BLOC, NOUVEAU_BLOC, 1)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    print("✅ Mentions légales corrigées avec succès.")
    print(f"   Sauvegarde créée : {FICHIER}.bak_mentions")


if __name__ == "__main__":
    main()
