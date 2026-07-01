#!/usr/bin/env python3
"""
Corrige les <h1> d'articles qui ont perdu des espaces (même bug que les
titres colles deja corriges sur index.html et le widget sim-card, mais
cette fois dans le H1 de la page article elle-meme, souvent structure
avec <br> et <em>).

Methode sure : pour chaque article, si le <h1> (texte visible, sans
balises) et le <title> (texte avant " — Economya.fr") contiennent
EXACTEMENT les memes caracteres une fois tous les espaces retires, alors
le <h1> a juste perdu des espaces que le <title> a gardes. Le script
insere les espaces manquants directement dans le HTML du <h1>, en PRESERVANT
les balises internes (<br>, <em>) a leur place exacte.

Si le contenu differe au-dela des espaces (vraie difference de texte,
ex: annee 2025 vs 2026, ou titre reformule), le fichier est SKIPPE et
liste separement pour revue manuelle.

Idempotent. Sauvegarde .bak_h1espaces avant modification.
"""

import glob
import re
import shutil

TITLE_RE = re.compile(r'<title>(.*?)\s*—\s*Economya\.fr</title>')
H1_RE = re.compile(r'<h1>(.*?)</h1>', re.DOTALL)


def extraire_texte_et_mapping(h1_interieur):
    texte = []
    mapping = []
    i = 0
    n = len(h1_interieur)
    while i < n:
        if h1_interieur[i] == '<':
            fin = h1_interieur.find('>', i)
            if fin == -1:
                break
            i = fin + 1
            continue
        texte.append(h1_interieur[i])
        i += 1
        mapping.append(i)
    return ''.join(texte), mapping


def inserer_espaces(h1_interieur, positions_insertion):
    resultat = h1_interieur
    for pos in sorted(positions_insertion, reverse=True):
        resultat = resultat[:pos] + ' ' + resultat[pos:]
    return resultat


def calculer_insertions(titre, texte_h1, mapping):
    insertions = []
    i, j = 0, 0
    while i < len(titre) and j < len(texte_h1):
        if titre[i] == texte_h1[j]:
            i += 1
            j += 1
        elif titre[i] == ' ':
            pos_raw = mapping[j] - 1 if j < len(mapping) else mapping[-1]
            insertions.append(pos_raw)
            i += 1
        elif texte_h1[j] == ' ':
            j += 1
        else:
            return None
    return insertions


def main():
    corriges = []
    ignores_diff_reelle = []
    ignores_erreur = []

    for fichier in sorted(glob.glob("article-*.html")):
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read()

        m_title = TITLE_RE.search(contenu)
        m_h1 = H1_RE.search(contenu)
        if not m_title or not m_h1:
            continue

        titre = m_title.group(1).strip()
        h1_interieur = m_h1.group(1)
        texte_h1, mapping = extraire_texte_et_mapping(h1_interieur)
        texte_h1_norm = re.sub(r'\s+', ' ', texte_h1).strip()

        if titre == texte_h1_norm:
            continue

        if titre.replace(" ", "") != texte_h1.replace(" ", "").strip():
            ignores_diff_reelle.append((fichier, titre, texte_h1_norm))
            continue

        insertions = calculer_insertions(titre, texte_h1, mapping)
        if insertions is None:
            ignores_erreur.append(fichier)
            continue

        nouveau_h1_interieur = inserer_espaces(h1_interieur, insertions)
        nouveau_h1 = f"<h1>{nouveau_h1_interieur}</h1>"
        contenu_modifie = contenu[:m_h1.start()] + nouveau_h1 + contenu[m_h1.end():]

        shutil.copy2(fichier, fichier + ".bak_h1espaces")
        with open(fichier, "w", encoding="utf-8") as f:
            f.write(contenu_modifie)
        corriges.append(fichier)

    print(f"OK {len(corriges)} fichier(s) corrige(s) automatiquement (espaces reinseres dans le h1)\n")

    if ignores_erreur:
        print(f"ATTENTION {len(ignores_erreur)} fichier(s) ignore(s) (desalignement, a verifier manuellement) :")
        for f in ignores_erreur:
            print(f"  {f}")
        print()

    if ignores_diff_reelle:
        print(f"INFO {len(ignores_diff_reelle)} fichier(s) avec vraie difference de texte (non touches) :\n")
        for f, t, h in ignores_diff_reelle:
            print(f"  {f}")
            print(f"    title: {t}")
            print(f"    h1   : {h}")


if __name__ == "__main__":
    main()
