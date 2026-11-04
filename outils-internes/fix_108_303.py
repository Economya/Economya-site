import shutil

# --- article-108 : badge saving-pill sans fond ---
f1 = "article-108.html"
c1 = open(f1, encoding='utf-8').read()
ancien1 = '<div class="saving-pill">🔒 Protection maximale à 0 €</div>'
nouveau1 = ('<div class="saving-pill" style="display:inline-flex;align-items:center;'
            'gap:.4rem;background:#EF9F27;color:white;font-weight:600;font-size:.9rem;'
            'padding:.5rem 1.2rem;border-radius:50px">🔒 Protection maximale à 0 €</div>')

if nouveau1 in c1:
    print(f"{f1} : deja corrige (idempotent)")
elif ancien1 in c1:
    c1_new = c1.replace(ancien1, nouveau1, 1)
    shutil.copy2(f1, f1 + '.bak_pill108')
    open(f1, 'w', encoding='utf-8').write(c1_new)
    print(f"{f1} : OK corrige")
else:
    print(f"{f1} : chaine non trouvee, verifier manuellement")

# --- article-303 : footer sans fond vert ---
f2 = "article-303.html"
c2 = open(f2, encoding='utf-8').read()
ancien2 = '<footer>'
nouveau2 = '<footer style="background:#085041;color:white;padding:2rem 1.5rem;text-align:center;margin-top:2rem">'

if 'data-footer-fixed' in c2:
    print(f"{f2} : deja corrige (idempotent)")
elif ancien2 in c2:
    c2_new = c2.replace(ancien2, '<footer data-footer-fixed="1" style="background:#085041;color:white;padding:2rem 1.5rem;text-align:center;margin-top:2rem">', 1)
    shutil.copy2(f2, f2 + '.bak_footer303')
    open(f2, 'w', encoding='utf-8').write(c2_new)
    print(f"{f2} : OK corrige")
else:
    print(f"{f2} : chaine non trouvee, verifier manuellement")
