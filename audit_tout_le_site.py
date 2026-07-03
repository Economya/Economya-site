import glob

# TOUS les fichiers html, pas juste article-*.html
fichiers = sorted(glob.glob('*.html'))
print(f"Total fichiers HTML sur le site : {len(fichiers)}\n")

sans_politique = []
sans_mentions = []
sans_contact = []
sans_footer_vert = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    if 'Politique de confidentialité' not in c and 'politique-confidentialite' not in c:
        sans_politique.append(f)
    if 'Mentions légales' not in c and 'mentions-legales' not in c:
        sans_mentions.append(f)
    if '>Contact<' not in c and 'contact.html' not in c and 'mailto:' not in c:
        sans_contact.append(f)
    # fond vert du footer (couleur connue #085041 ou variable --gd)
    if '#085041' not in c and 'background:var(--gd)' not in c and 'background: var(--gd)' not in c:
        sans_footer_vert.append(f)

print(f"Sans lien Politique de confidentialite : {len(sans_politique)}")
print(sans_politique)
print()
print(f"Sans lien Mentions legales : {len(sans_mentions)}")
print(sans_mentions)
print()
print(f"Sans lien/mention Contact : {len(sans_contact)}")
print(sans_contact)
print()
print(f"Sans fond vert #085041 dans le footer : {len(sans_footer_vert)}")
print(sans_footer_vert)
