#!/usr/bin/env python3
"""
Corrige 2 erreurs factuelles trouvées lors de l'audit qualité aléatoire :

1. article-489.html : "La Bourse French Tech (anciennement Bourse à l'Émergence)"
   -> faux : la Bourse French Tech Emergence est le nom ACTUEL (toujours active
   sur bpifrance.fr en 2026), pas un ancien nom. Ce sont 2 dispositifs distincts
   qui coexistent (Bourse French Tech / Bourse French Tech Emergence).

2. article-245.html : statistiques du don d'organes obsolètes/erronées.
   Sources vérifiées : Agence de la biomédecine, bilan 2025 (publié 2026).
   - "22 personnes/jour reçoivent une greffe" -> ~17/jour (chiffre réel 2024-2025)
   - "25 000 personnes en attente" -> 23 294 (1er janvier 2026)
   - "99% des Français favorables" -> ~80% (8 Français sur 10) selon l'Agence
     de la biomédecine — écart significatif, à corriger en priorité
   - "35% l'ont signalé à leurs proches" -> ~49% (1 Français sur 2)

Idempotent : si déjà corrigé, ne fait rien.
Sauvegarde .bak_auditqualite avant modification de chaque fichier.
"""

import os
import shutil

CORRECTIONS = {
    "article-489.html": [
        (
            "La Bourse French Tech (anciennement Bourse à l'Émergence) est une aide de 5 000 à 30 000 € pour les startups en phase d'idée ou d'amorçage.",
            "La Bourse French Tech Emergence est une aide de 5 000 à 30 000 € pour les startups en phase d'idée ou d'amorçage (à ne pas confondre avec la Bourse French Tech classique, dispositif distinct).",
        ),
    ],
    "article-245.html": [
        (
            "En France, chaque jour, 22 personnes reçoivent un organe qui leur sauve la vie — et 3 meurent faute de greffon disponible.",
            "En France, chaque jour, environ 17 personnes reçoivent un organe qui leur sauve la vie — et 3 meurent faute de greffon disponible.",
        ),
        (
            '<div class="stat-cell"><span class="stat-num">25 000</span><span class="stat-lbl">personnes en attente de greffe</span></div>',
            '<div class="stat-cell"><span class="stat-num">23 294</span><span class="stat-lbl">personnes en attente de greffe</span></div>',
        ),
        (
            '<div class="stat-cell"><span class="stat-num">22/jour</span><span class="stat-lbl">greffes réalisées en moyenne</span></div>',
            '<div class="stat-cell"><span class="stat-num">17/jour</span><span class="stat-lbl">greffes réalisées en moyenne</span></div>',
        ),
        (
            '<div class="stat-cell"><span class="stat-num">99 %</span><span class="stat-lbl">des Français favorables au don*</span></div>',
            '<div class="stat-cell"><span class="stat-num">80 %</span><span class="stat-lbl">des Français favorables au don*</span></div>',
        ),
        (
            "* Selon les sondages IFOP — mais seulement 35 % l'ont signalé à leurs proches.",
            "* Selon l'Agence de la biomédecine — mais seulement 49 % (1 Français sur 2) l'ont signalé à leurs proches.",
        ),
    ],
}


def corriger_fichier(fichier, remplacements):
    if not os.path.exists(fichier):
        print(f"❌ Fichier introuvable : {fichier} (ignoré)")
        return

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    contenu_modifie = contenu
    total = 0

    for ancien, nouveau in remplacements:
        if ancien in contenu_modifie:
            contenu_modifie = contenu_modifie.replace(ancien, nouveau, 1)
            print(f"  ✅ Corrigé : {ancien[:55]}...")
            total += 1
        elif nouveau in contenu_modifie:
            print(f"  ℹ️  Déjà corrigé (idempotent) : {nouveau[:55]}...")
        else:
            print(f"  ⚠️  Chaîne non trouvée : {ancien[:55]}...")

    if total == 0:
        print(f"  → Rien à faire pour {fichier}.")
        return

    shutil.copy2(fichier, fichier + ".bak_auditqualite")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu_modifie)
    print(f"  → {total} correction(s) écrite(s) dans {fichier} (sauvegarde créée)\n")


def main():
    for fichier, remplacements in CORRECTIONS.items():
        print(f"=== {fichier} ===")
        corriger_fichier(fichier, remplacements)


if __name__ == "__main__":
    main()
