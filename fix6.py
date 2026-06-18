{\rtf1\ansi\ansicpg1252\cocoartf2759
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
\
count = 0\
old = '<button class="hamburger" onclick="toggleMenu()" aria-label="Menu"><span></span><span></span><span></span></button><div class="mobile-menu" id="mobileMenu"><button class="close-btn" onclick="toggleMenu()">X</button><a href="index.html">Accueil</a><a href="jeux.html">Jeux</a><a href="outils-gratuits.html">Outils gratuits</a><a href="comparateurs.html">Comparateurs</a><a href="a-propos.html">A propos</a><a href="recherche.html">Rechercher</a></div></nav>'\
\
new = '</nav><button class="hamburger" onclick="toggleMenu()" aria-label="Menu"><span></span><span></span><span></span></button><div class="mobile-menu" id="mobileMenu"><button class="close-btn" onclick="toggleMenu()">X</button><a href="index.html">Accueil</a><a href="jeux.html">Jeux</a><a href="outils-gratuits.html">Outils gratuits</a><a href="comparateurs.html">Comparateurs</a><a href="a-propos.html">A propos</a><a href="recherche.html">Rechercher</a></div>'\
\
for f in os.listdir('.'):\
    if not f.endswith('.html') or f == 'index.html':\
        continue}