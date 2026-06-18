import os
L='https://www.awin1.com/cread.php?awinmid=101873&awinaffid=2926395'
P='<p>Visitez <a href="'+L+'">EUROCOC</a> pour votre certificat europeen.</p>'
A=['article-270.html','article-56.html','article-149.html','article-215.html','article-263.html','article-269.html','article-176.html']
for f in A:
    c=open(f,'r',encoding='utf-8',errors='ignore').read()
    if L not in c:open(f,'w',encoding='utf-8').write(c.replace('</footer>',P+'</footer>',1))
print('done')

