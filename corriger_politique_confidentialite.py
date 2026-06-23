#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction de la politique de confidentialité — politique-confidentialite.html
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

1. Remplace "L'équipe Economya" par un renvoi vers les mentions légales (cohérent avec la correction déjà faite)
2. Harmonise la durée de conservation Google Analytics (13 mois partout, au lieu de 13 et 14 mélangés)

Sans danger à relancer (idempotent). Sauvegarde en .bak_politique avant modification.

Usage :
    python3 corriger_politique_confidentialite.py
"""

import os

FICHIER = "politique-confidentialite.html"

ANCIEN_RESPONSABLE = '''  <h2>1. Responsable du traitement</h2>
  <p><strong>L'équipe Economya</strong> — éditeur du site Economya.fr<br>
  Contact : <a href="mailto:contact@economya.fr">contact@economya.fr</a></p>'''

NOUVEAU_RESPONSABLE = '''  <h2>1. Responsable du traitement</h2>
  <p>Le responsable du traitement des données décrites dans cette politique est l'éditeur du site Economya.fr, dont l'identité figure dans nos <a href="mentions-legales.html">mentions légales</a>.<br>
  Contact : <a href="mailto:contact@economya.fr">contact@economya.fr</a></p>'''

ANCIENNE_DUREE = "Données de navigation : 14 mois (Google Analytics)"
NOUVELLE_DUREE = "Données de navigation : 13 mois (Google Analytics)"


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier {FICHIER} introuvable dans ce dossier.")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        contenu = f.read()

    contenu_original = contenu
    modifications = []

    if "mentions-legales.html\">mentions légales</a>" in contenu and "Responsable du traitement" in contenu:
        print("✅ Déjà corrigé (responsable du traitement) — aucune modification nécessaire sur ce point.")
    elif ANCIEN_RESPONSABLE in contenu:
        contenu = contenu.replace(ANCIEN_RESPONSABLE, NOUVEAU_RESPONSABLE, 1)
        modifications.append("Responsable du traitement corrigé")
    else:
        print("⚠️  Bloc 'Responsable du traitement' non trouvé tel qu'attendu — à vérifier manuellement.")

    if ANCIENNE_DUREE in contenu:
        contenu = contenu.replace(ANCIENNE_DUREE, NOUVELLE_DUREE, 1)
        modifications.append("Durée de conservation harmonisée (13 mois)")

    if contenu == contenu_original:
        print("Aucune modification supplémentaire effectuée.")
        return

    with open(FICHIER + ".bak_politique", 'w', encoding='utf-8') as f:
        f.write(contenu_original)

    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.write(contenu)

    print(f"✅ Politique de confidentialité corrigée : {', '.join(modifications)}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_politique")


if __name__ == "__main__":
    main()
