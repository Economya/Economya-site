import os

dossier = os.path.dirname(os.path.abspath(__file__))

ga_code = (
    "<!-- Google Analytics -->\n"
    "<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-YBK8GHCDT5\"></script>\n"
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  gtag('js', new Date());\n"
    "  gtag('config', 'G-YBK8GHCDT5');\n"
    "</script>\n"
)

fichiers = [f for f in os.listdir(dossier) if f.endswith('.html')]
modifies = 0
deja = 0

for nom in fichiers:
    chemin = os.path.join(dossier, nom)
    with open(chemin, 'r', encoding='utf-8') as f:
        contenu = f.read()
    if 'G-YBK8GHCDT5' in contenu:
        deja += 1
        continue
    nouveau = contenu.replace('</head>', ga_code + '</head>', 1)
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(nouveau)
    modifies += 1

print(f"✅ {modifies} fichiers mis à jour avec Google Analytics")
print(f"ℹ️  {deja} fichiers avaient déjà le code")
input("\nAppuyez sur Entrée pour fermer...")
