import os
old='<div class="nlform"><input type="email" placeholder="votre@email.fr"/><button>Je m\'abonne</button></div>'
new='<form method="POST" action="https://8c3516b5.sibforms.com/serve/MUIFAJ7Uw5h5Fjb8WPWvxzffQ8pcvJ7gIdeCWQHWqGm-ovG94xuIqP1HX7FWoPMTkBLZz6o-pkHCgDxXe7D_2o4X0BwLHldjyE3p6jqiajS2rYCpWpdRI44saG6YZ-m_jwv-SVXVmMm8PMkQ9Dh0rZ0X_hQg3UC3KKqm8CeDvvkj1CLAR3IBPt6ZOLCLgEOOtsFOzYGVT6MINtcZOQ=="><input type="email" name="EMAIL" placeholder="votre@email.fr" required/><input type="hidden" name="locale" value="fr"><button type="submit">Je m\'abonne</button></form>'
for f in os.listdir('.'):
c=open(f,'r',encoding='utf-8',errors='ignore').read()
if old in c:
open(f,'w',encoding='utf-8').write(c.replace(old,new,1))
print('done')
print('done')

