import glob

fichiers = sorted(glob.glob('article-*.html'))
print(f"Total articles : {len(fichiers)}\n")

vraiment_incomplets = []

for f in fichiers:
    c = open(f, encoding='utf-8').read()
    idx = c.find('<footer')
    if idx == -1:
        vraiment_incomplets.append((f, "AUCUNE BALISE FOOTER"))
        continue
    bloc = c[idx:idx+500]
    a_mentions = 'Mentions légales' in bloc or 'mentions-legales' in bloc
    a_contact = 'Contact' in bloc or 'contact.html' in bloc or 'contact@' in bloc
    if not (a_mentions and a_contact):
        raison = []
        if not a_mentions:
            raison.append("pas de Mentions legales")
        if not a_contact:
            raison.append("pas de Contact")
        vraiment_incomplets.append((f, " + ".join(raison)))

print(f"VRAIMENT incomplets : {len(vraiment_incomplets)}")
for f, raison in vraiment_incomplets:
    print(f"  {f} : {raison}")
