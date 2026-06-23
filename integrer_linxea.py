#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intégration du bloc partenaire Linxea sur les articles pertinents
À lancer UNE SEULE FOIS depuis le dossier ~/Desktop/mon site

Insère le bloc Linxea juste avant le marqueur "<!-- Boutons partage -->",
présent de façon constante en fin d'article sur le site.

Idempotent. Sauvegarde en .bak_linxea avant modification.

Usage :
    python3 integrer_linxea.py
"""

import os

FICHIERS = [
    "article-100.html",
    "article-340.html",
    "article-337.html",
    "article-339.html",
    "article-341.html",
    "article-439.html",
    "article-449.html",
    "article-462.html",
]

MARQUEUR = "<!-- Boutons partage -->"

BLOC_LINXEA = '''<!-- Partenaire Linxea -->
<div style="background:linear-gradient(135deg,#FAEEDA,#FFF8EE);border:1px solid #EF9F27;border-radius:16px;padding:1.2rem 1.5rem;margin:2rem 0;display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
  <span style="font-size:2rem">📈</span>
  <div style="flex:1;min-width:200px">
    <div style="font-weight:700;color:#633806;font-size:.95rem;margin-bottom:.2rem">Optimisez votre épargne avec Linxea</div>
    <div style="font-size:.82rem;color:#5F5E5A">Assurance-vie et épargne retraite à frais réduits, courtier ORIAS depuis 2001. Les unités de compte comportent un risque de perte en capital ; le fonds en euros est garanti.</div>
  </div>
  <a href="https://www.awin1.com/cread.php?awinmid=13275&awinaffid=2926395&ued=https%3A%2F%2Fwww.linxea.com" target="_blank" rel="noopener sponsored" style="background:#EF9F27;color:white;padding:.6rem 1.2rem;border-radius:50px;font-weight:700;font-size:.82rem;text-decoration:none;white-space:nowrap">Découvrir →</a>
</div>

'''


def traiter_fichier(chemin):
    if not os.path.exists(chemin):
        return "introuvable"

    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()

    if "Partenaire Linxea" in contenu:
        return "déjà présent"

    if MARQUEUR not in contenu:
        return "marqueur absent"

    with open(chemin + ".bak_linxea", 'w', encoding='utf-8') as f:
        f.write(contenu)

    nouveau_contenu = contenu.replace(MARQUEUR, BLOC_LINXEA + MARQUEUR, 1)

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
    print(f"Marqueur absent (structure différente) : {resultats['marqueur absent']}")
    print(f"\nSauvegardes créées avec l'extension .bak_linxea")


if __name__ == "__main__":
    main()
