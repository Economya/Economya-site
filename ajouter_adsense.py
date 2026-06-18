import os

dossier = os.path.dirname(os.path.abspath(__file__))

adsense_code = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3051071564398795"\n'
    '     crossorigin="anonymous"></script>\n'
)

fichiers = [f for f in os.listdir(dossier) if f.endswith('.html')]
modifies = 0
deja = 0

for nom in fichiers:
    chemin = os.path.join(dossier, nom)
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if 'ca-pub-3051071564398795' in contenu:
        deja += 1
        continue
    nouveau = contenu.replace('</head>', adsense_code + '</head>', 1)
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    modifies += 1

print(f"✅ {modifies} fichiers mis à jour avec le code AdSense")
print(f"ℹ️  {deja} fichiers avaient déjà le code")
input("\nAppuyez sur Entrée pour fermer...")
