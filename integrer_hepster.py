#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du bloc partenaire Hepster
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Formulation volontairement neutre : ni promesse de fiabilité, ni mention
des avis mitigés. Description factuelle du produit uniquement.

Idempotent. Sauvegarde en .bak_hepster avant modification.

Usage :
    python3 integrer_hepster.py
"""

import os

FICHIERS = [
    "article-11.html",
    "article-23.html",
    "article-248.html",
    "article-255.html",
    "article-490.html",
]

MARQUEUR = "<!-- Boutons partage -->"

BLOC_HEPSTER = '''<!-- Partenaire Hepster -->
<div style="background:linear-gradient(135deg,#E1F5EE,#f0fdf4);border:1px solid #1D9E75;border-radius:16px;padding:1.2rem 1.5rem;margin:2rem 0;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
  <span style="font-size:2rem">🚲</span>
  <div style="flex:1;min-width:200px">
    <div style="font-weight:700;color:#085041;font-size:.95rem;margin-bottom:.2rem">Assurer vos appareils avec Hepster</div>
    <div style="font-size:.82rem;color:#5F5E5A">Assurance vélo, trottinette et appareils électroniques. Couverture vol, casse et oxydation.</div>
  </div>
  <a href="https://www.awin1.com/cread.php?awinmid=30643&awinaffid=2926395&ued=https%3A%2F%2Fwww.hepster.com%2Ffr" target="_blank" rel="noopener sponsored" style="background:#1D9E75;color:white;padding:.6rem 1.2rem;border-radius:50px;font-weight:700;font-size:.82rem;text-decoration:none;white-space:nowrap">Découvrir →</a>
</div>

'''


def traiter_fichier(chemin):
    if not os.path.exists(chemin):
        return "introuvable"

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "Partenaire Hepster" in contenu:
        return "déjà présent"

    if MARQUEUR not in contenu:
        return "marqueur absent"

    with open(chemin + ".bak_hepster", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(MARQUEUR, BLOC_HEPSTER + MARQUEUR, 1)

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau_contenu)

    return "ajouté"


def main():
    resultats = {"ajouté": 0, "déjà présent": 0, "introuvable": 0, "marqueur absent": 0}
    details = []

    for fichier in FICHIERS:
        statut = traiter_fichier(fichier)
        resultats[statut] += 1
        details.append(f"{fichier} : {statut}")

    print("\n".join(details))
    print(f"\n=== RÉSUMÉ ===")
    print(f"Ajoutés : {resultats['ajouté']}")
    print(f"Déjà présents : {resultats['déjà présent']}")
    print(f"Introuvables : {resultats['introuvable']}")
    print(f"Marqueur absent : {resultats['marqueur absent']}")


if __name__ == "__main__":
    main()
