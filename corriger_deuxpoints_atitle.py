#!/usr/bin/env python3
"""
Corrige le bug d'espace manquant après les deux-points dans les titres de cartes
d'index.html (balises <div class="atitle">...</div>).

Exemple : "Soins dentaires :réduire la facture" -> "Soins dentaires : réduire la facture"

Le correctif est strictement scopé au contenu des balises atitle, pour ne jamais
toucher au CSS (ex: color:red) ou au JS du fichier.

Idempotent : relancer sur un fichier déjà corrigé ne change rien.
Sauvegarde .bak_deuxpoints_atitle avant modification.
"""

import os
import re
import shutil

FICHIER = "index.html"

# Motif : un espace, un deux-points, directement suivi d'une lettre (pas d'espace après)
MOTIF_MANQUE = re.compile(r' :([a-zàâäéèêëïîôöùûüçA-ZÀÂÄÉÈÊËÏÎÔÖÙÛÜÇ])')


def main():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, "r", encoding="utf-8") as f:
        contenu = f.read()

    # On ne touche qu'à l'intérieur des balises <div class="atitle">...</div>
    pattern_atitle = re.compile(r'<div class="atitle">.*?</div>')

    nb_corrections = [0]

    def remplacer(match):
        original = match.group(0)
        corrige = MOTIF_MANQUE.sub(r' : \1', original)
        if corrige != original:
            nb_corrections[0] += 1
        return corrige

    contenu_modifie = pattern_atitle.sub(remplacer, contenu)

    if nb_corrections[0] == 0:
        print("✅ Rien à faire — tous les titres atitle sont déjà corrects (idempotent).")
        return

    shutil.copy2(FICHIER, FICHIER + ".bak_deuxpoints_atitle")
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)

    print(f"✅ {nb_corrections[0]} titre(s) corrigé(s) dans {FICHIER}")
    print(f"   Sauvegarde créée : {FICHIER}.bak_deuxpoints_atitle")


if __name__ == "__main__":
    main()
