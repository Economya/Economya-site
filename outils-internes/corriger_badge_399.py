import re, shutil

FICHIER = "article-399.html"
ANCIEN = '💰 Jusqu\'à 00 000 €'
ANCIEN_ALT = '💰 00 000 €'
NOUVEAU = "💰 Calculez vos vraies économies"

c = open(FICHIER, encoding='utf-8').read()

if NOUVEAU in c:
    print("Deja corrige (idempotent).")
else:
    if ANCIEN in c:
        c_new = c.replace(ANCIEN, NOUVEAU, 1)
    elif ANCIEN_ALT in c:
        c_new = c.replace(ANCIEN_ALT, NOUVEAU, 1)
    else:
        print("Chaine non trouvee, verifiez le contenu exact du badge.")
        c_new = None

    if c_new:
        shutil.copy2(FICHIER, FICHIER + '.bak_badge399')
        open(FICHIER, 'w', encoding='utf-8').write(c_new)
        print(f"OK : badge corrige -> '{NOUVEAU}'")
