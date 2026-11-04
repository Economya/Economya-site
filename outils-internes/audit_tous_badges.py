import re, glob

fichiers = sorted(glob.glob('article-*.html'))
suspects = []

MOTS_PLACEHOLDER = ['somme', 'montant', 'chiffre', 'xxx', 'todo', 'valeur', 'placeholder', 'nombre']

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    for m in re.finditer(r'class="savings-badge"[^>]*>([^<]*)</div>', c):
        texte = m.group(1).strip()
        a_chiffre = bool(re.search(r'\d', texte))
        a_mot_suspect = any(mot in texte.lower() for mot in MOTS_PLACEHOLDER)
        if not a_chiffre or a_mot_suspect:
            suspects.append((f, texte))

print(f"{len(suspects)} badges suspects trouves (pas de chiffre ou mot placeholder)\n")
for f, texte in suspects:
    print(f"{f:22s} : {texte!r}")
