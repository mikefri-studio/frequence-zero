# add_teaser_suite.py — scène post-générique : teaser d'une suite
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

TEASER_HTML = '''
  <!-- TEASER SUITE -->
  <section class="ecran" id="ecran-teaser">
    <div class="contenu carte generique">
      <p class="teaser-quand">Six mois plus tard — une autre ville.</p>
      <div class="crt">STATION : RADIO NUIT CLAIRE<br>HEURE : 23 h 58<br>APPEL ENTRANT : …</div>
      <p class="fin-texte">Le standard affiche un numéro que personne n'utilise plus depuis vingt ans.</p>
      <p class="teaser-zero">LIGNE 0</p>
      <p class="a-suivre">À suivre…</p>
      <button class="btn petit" id="btn-teaser-fin">📻 Éteindre le poste</button>
    </div>
  </section>
'''

LIEN_TEASER = '\n        <button class="lien" id="btn-teaser">📡 Un dernier grésillement…</button>'

PS_ARTICLE = '''        <p class="j-ps">P.S. — À quatre cents kilomètres de là, une autre station de nuit signale le même grésillement sur sa ligne interne. La direction dément.</p>
'''

TEASER_CSS = '''
/* ----- teaser suite ----- */
.teaser-quand { color: var(--gris-texte); font-style: italic; letter-spacing: .12em; margin-bottom: 14px; }
.teaser-zero { font-size: clamp(1.6rem, 6vw, 3rem); color: var(--rouge); letter-spacing: .4em; text-shadow: 0 0 12px var(--rouge), 0 0 40px var(--rouge); animation: neon 2.2s infinite; margin: 10px 0 18px; }
.j-ps { margin-top: 12px; font-size: .85rem; color: #6b6353; font-style: italic; border-top: 1px solid #c9c2ae; padding-top: 8px; }
'''

TEASER_JS = '''
/* ---------- TEASER SUITE ---------- */
const btnTeaser = $("#btn-teaser");
if (btnTeaser) btnTeaser.onclick = () => { montrer("#ecran-teaser"); gresillement(2.5, 0.04); jouerMorse("ASUIVRE"); };
const btnTeaserFin = $("#btn-teaser-fin");
if (btnTeaserFin) btnTeaserFin.onclick = () => { delete document.body.dataset.nuit; rendreTitre(); montrer("#ecran-titre"); };
'''

# --- 1. index.html : lien discret dans le générique + section teaser ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "ecran-teaser" in html:
    print("⏭️  index.html déjà modifié")
else:
    cible = '<button class="btn petit" id="btn-titre2">🏠 Titre</button>'
    if cible not in html:
        sys.exit("❌ Générique absent. Lance d'abord : python3 add_generique.py")
    html = html.replace(cible, cible + LIEN_TEASER, 1)
    if "</main>" not in html:
        sys.exit("❌ Balise </main> introuvable dans index.html")
    html = html.replace("</main>", TEASER_HTML + "</main>", 1)
    ecrire(f, html)
    print("✅ index.html")

# --- 2. index.html (bis) : P.S. dans l'article de journal ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "j-ps" in html:
    print("⏭️  P.S. déjà présent")
elif '<p class="j-sign">' in html:
    ecrire(f, html.replace('<p class="j-sign">', PS_ARTICLE + '      <p class="j-sign">', 1))
    print("✅ P.S. ajouté à l'article")
else:
    print("⚠️  Article absent — P.S. ignoré (lance add_epilogue.py d'abord si tu veux l'article)")

# --- 3. style.css ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
if "teaser suite" in c:
    print("⏭️  css/style.css déjà modifié")
else:
    ecrire(f, c + TEASER_CSS)
    print("✅ css/style.css")

# --- 4. game.js ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
if "TEASER SUITE" in c:
    print("⏭️  js/game.js déjà modifié")
else:
    ecrire(f, c + TEASER_JS)
    print("✅ js/game.js")

print("\n📡 Teaser de suite intégré !")
print('git add . && git commit -m "📡 Scène post-générique : teaser de la suite" && git push')