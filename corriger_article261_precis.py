#!/usr/bin/env python3
"""
Corrige uniquement la ligne d'article-261.html qui mentionne explicitement
"Leasing social" avec le seuil de revenu, confirme a 16 880 euros
(les mentions "bonus majore" du bonus ecologique lui-meme, distinctes,
ne sont pas touchees faute de verification separee de leur propre seuil).

Idempotent. Sauvegarde .bak_precis avant modification.
"""

import os
import shutil

FICHIER = "article-261.html"
ANCIEN = '<tr><td>Leasing social</td><td class="g">100 € à 150 €/mois pour les éligibles (revenus ≤ 15 400 €)</td></tr>'
NOUVEAU = '<tr><td>Leasing social</td><td class="g">100 € à 150 €/mois pour les éligibles (revenus ≤ 16 880 €)</td></tr>'


def main():
    if not os.path.exists(FICHIER):
        print(f"Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    if NOUVEAU in contenu:
        print("Rien a faire - deja corrige (idempotent).")
        return

    if ANCIEN not in contenu:
        print("Chaine non trouvee. Verifiez manuellement avec :")
        print("  grep -n 'Leasing social.*15 400' article-261.html")
        return

    contenu_modifie = contenu.replace(ANCIEN, NOUVEAU, 1)

    shutil.copy2(FICHIER, FICHIER + ".bak_precis")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"OK corrige dans {FICHIER}")
    print("   15 400 -> 16 880 (uniquement pour la ligne Leasing social)")


if __name__ == "__main__":
    main()
