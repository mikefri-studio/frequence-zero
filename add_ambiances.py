# add_ambiances.py — décors de fond différents selon la nuit (v2 - fix indentation)
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

# --- socle dessins (ajouté seulement s'il manque) ---
DESSINS_BASE = '''
/* ============ DESSINS D'AMBIANCE (SVG intégrés) ============ */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 6;
  pointer-events: none;
  opacity: .55;
  background:
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><defs><mask id='m'><rect width='200' height='200' fill='white'/><circle cx='128' cy='78' r='40' fill='black'/></mask></defs><circle cx='105' cy='95' r='44' fill='%23ffb340' opacity='.75' mask='url(%23m)'/><g stroke='%23dfe7ee' stroke-width='2' opacity='.7' stroke-linecap='round'><path d='M38 52 v12 M32 58 h12'/><path d='M60 142 v9 M55.5 146.5 h9'/><path d='M24 104 v7 M20.5 107.5 h7'/></g></svg>") top right / 170px 170px no-repeat,
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><g stroke='%23ff3b30' fill='none' stroke-width='2.5' opacity='.6' stroke-linecap='round'><path d='M100 192 V92'/><path d='M84 192 L100 148 L116 192'/><path d='M100 122 L88 152 M100 122 L112 152'/><circle cx='100' cy='86' r='4' fill='%23ff3b30'/><path d='M78 64 a31 31 0 0 1 44 0'/><path d='M66 52 a48 48 0 0 1 68 0'/><path d='M54 40 a65 65 0 0 1 92 0'/></g></svg>") bottom left / 180px 180px no-repeat;
}
'''

# --- déclinaisons par nuit ---
AMBIANCES = '''
/* ============ AMBIANCES PAR NUIT ============ */

/* NUIT 1 — lune + route sous la pluie */
body[data-nuit="1"]::before {
  background:
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><defs><mask id='m'><rect width='200' height='200' fill='white'/><circle cx='128' cy='78' r='40' fill='black'/></mask></defs><circle cx='105' cy='95' r='44' fill='%23ffb340' opacity='.75' mask='url(%23m)'/><g stroke='%23dfe7ee' stroke-width='2' opacity='.7' stroke-linecap='round'><path d='M38 52 v12 M32 58 h12'/><path d='M60 142 v9 M55.5 146.5 h9'/><path d='M24 104 v7 M20.5 107.5 h7'/></g></svg>") top right / 170px 170px no-repeat,
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><g stroke='%239fb0c0' fill='none' stroke-width='2.5' opacity='.55' stroke-linecap='round'><path d='M40 190 L92 96'/><path d='M160 190 L108 96'/><path d='M100 178 v-14 M100 148 v-14 M100 118 v-10'/></g></svg>") bottom left / 180px 180px no-repeat;
}

/* NUIT 2 — entrepôt Mirabeau + camionnette */
body[data-nuit="2"]::before {
  background:
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><g stroke='%2339ff88' fill='none' stroke-width='2.5' opacity='.5' stroke-linejoin='round'><path d='M40 155 V82 L100 52 L160 82 V155 Z'/><path d='M72 155 V104 H128 V155'/><path d='M72 120 H128 M72 137 H128'/></g><rect x='136' y='90' width='14' height='12' fill='%23ffb340' opacity='.75'/></svg>") top right / 170px 170px no-repeat,
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><g stroke='%2339ff88' fill='none' stroke-width='2.5' opacity='.5' stroke-linecap='round' stroke-linejoin='round'><path d='M28 148 V108 H118 L150 124 V148 Z'/><path d='M118 108 V124 H150'/><circle cx='58' cy='150' r='10'/><circle cx='124' cy='150' r='10'/><path d='M40 128 h44' stroke='%23ffb340' opacity='.8'/></g></svg>") bottom left / 180px 180px no-repeat;
}
body[data-nuit="2"] #pluie { background: repeating-linear-gradient(115deg, transparent 0 6px, rgba(120,255,180,.05) 6px 7px); }
body[data-nuit="2"]::after { background:
  linear-gradient(var(--vert), var(--vert)) top left / 26px 2px, linear-gradient(var(--vert), var(--vert)) top left / 2px 26px,
  linear-gradient(var(--vert), var(--vert)) top right / 26px 2px, linear-gradient(var(--vert), var(--vert)) top right / 2px 26px,
  linear-gradient(var(--vert), var(--vert)) bottom left / 26px 2px, linear-gradient(var(--vert), var(--vert)) bottom left / 2px 26px,
  linear-gradient(var(--vert), var(--vert)) bottom right / 26px 2px, linear-gradient(var(--vert), var(--vert)) bottom right / 2px 26px;
  background-repeat: no-repeat; }

/* NUIT 3 — flamme + cabine brûlée */
body[data-nuit="3"]::before {
  background:
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><g fill='none' stroke-linecap='round'><path d='M100 162 C68 132 78 100 100 68 C96 100 122 100 112 76 C134 108 132 134 100 162 Z' stroke='%23ff3b30' stroke-width='2.5' opacity='.6'/><path d='M100 150 C88 132 92 116 100 102 C108 116 112 132 100 150 Z' stroke='%23ffb340' stroke-width='2' opacity='.7'/></g><g fill='%23ffb340' opacity='.7'><circle cx='58' cy='78' r='2'/><circle cx='142' cy='58' r='1.5'/><circle cx='152' cy='112' r='2'/><circle cx='48' cy='122' r='1.5'/></g></svg>") top right / 170px 170px no-repeat,
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><g stroke='%23ff3b30' fill='none' stroke-width='2.5' opacity='.5' stroke-linecap='round'><path d='M60 162 V112 H140 V162'/><path d='M60 112 L100 86 L140 112'/><path d='M94 162 V132 H120 V162'/></g><path d='M100 82 C96 68 108 62 104 48 C116 58 108 68 112 76' stroke='%239fb0c0' fill='none' stroke-width='2' opacity='.5' stroke-linecap='round'/></svg>") bottom left / 180px 180px no-repeat;
}
body[data-nuit="3"] #pluie { background: repeating-linear-gradient(115deg, transparent 0 6px, rgba(255,120,80,.07) 6px 7px); }
body[data-nuit="3"]::after { background:
  linear-gradient(var(--rouge), var(--rouge)) top left / 26px 2px, linear-gradient(var(--rouge), var(--rouge)) top left / 2px 26px,
  linear-gradient(var(--rouge), var(--rouge)) top right / 26px 2px, linear-gradient(var(--rouge), var(--rouge)) top right / 2px 26px,
  linear-gradient(var(--rouge), var(--rouge)) bottom left / 26px 2px, linear-gradient(var(--rouge), var(--rouge)) bottom left / 2px 26px,
  linear-gradient(var(--rouge), var(--rouge)) bottom right / 26px 2px, linear-gradient(var(--rouge), var(--rouge)) bottom right / 2px 26px;
  background-repeat: no-repeat; }

/* NUIT 4 — porte ouverte + micro */
body[data-nuit="4"]::before {
  background:
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><path d='M128 76 L178 100 V162 H128 Z' fill='%23ffb340' opacity='.12'/><g stroke='%23dfe7ee' fill='none' stroke-width='2.5' opacity='.6' stroke-linecap='round' stroke-linejoin='round'><path d='M70 162 V60 H128 V162'/><path d='M128 60 L158 74 V162'/><path d='M70 162 H158'/><path d='M136 118 v10' stroke='%23ffb340'/></g></svg>") top right / 170px 170px no-repeat,
    url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><g stroke='%23dfe7ee' fill='none' stroke-width='2.5' opacity='.6' stroke-linecap='round'><rect x='88' y='58' width='24' height='42' rx='12'/><path d='M78 90 a22 22 0 0 0 44 0'/><path d='M100 112 V152 M78 152 H122'/></g><circle cx='100' cy='70' r='3' fill='%23ff3b30' opacity='.8'/></svg>") bottom left / 180px 180px no-repeat;
}
body[data-nuit="4"] #pluie { background: repeating-linear-gradient(115deg, transparent 0 6px, rgba(223,231,238,.05) 6px 7px); }
body[data-nuit="4"]::after { background:
  linear-gradient(var(--gris-texte), var(--gris-texte)) top left / 26px 2px, linear-gradient(var(--gris-texte), var(--gris-texte)) top left / 2px 26px,
  linear-gradient(var(--gris-texte), var(--gris-texte)) top right / 26px 2px, linear-gradient(var(--gris-texte), var(--gris-texte)) top right / 2px 26px,
  linear-gradient(var(--gris-texte), var(--gris-texte)) bottom left / 26px 2px, linear-gradient(var(--gris-texte), var(--gris-texte)) bottom left / 2px 26px,
  linear-gradient(var(--gris-texte), var(--gris-texte)) bottom right / 26px 2px, linear-gradient(var(--gris-texte), var(--gris-texte)) bottom right / 2px 26px;
  background-repeat: no-repeat; }
'''

# --- 1. game.js : pose data-nuit au démarrage, l'efface au titre ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
modif = False

# data-nuit au démarrage
if "dataset.nuit" not in c:
    cible = "  indexNuit = i; nuit = NUITS[i];"
    if cible not in c:
        sys.exit("❌ Ligne indexNuit introuvable dans game.js")
    c = c.replace(cible, cible + "\n  document.body.dataset.nuit = i + 1;", 1)
    modif = True

# effacement au retour titre (tolérant aux espaces)
if "delete document.body.dataset.nuit" not in c:
    cible1 = '  $("#btn-titre").onclick = () => { rendreTitre(); montrer("#ecran-titre"); };'
    cible2 = '$("#btn-titre").onclick = () => { rendreTitre(); montrer("#ecran-titre"); };'
    
    if cible1 in c:
        c = c.replace(cible1, '  $("#btn-titre").onclick = () => { delete document.body.dataset.nuit; rendreTitre(); montrer("#ecran-titre"); };', 1)
        modif = True
    elif cible2 in c:
        c = c.replace(cible2, '$("#btn-titre").onclick = () => { delete document.body.dataset.nuit; rendreTitre(); montrer("#ecran-titre"); };', 1)
        modif = True
    else:
        sys.exit("❌ Handler btn-titre introuvable dans game.js")

if modif:
    ecrire(f, c)
    print("✅ js/game.js")
else:
    print("⏭️  js/game.js déjà modifié")

# --- 2. style.css : socle dessins (si besoin) + ambiances par nuit ---
f = os.path.join(BASE, "css", "style.css")
c = lire(f)
modif = False
if "DESSINS D'AMBIANCE" not in c:
    c += DESSINS_BASE
    modif = True
    print("✅ socle dessins ajouté")
if "AMBIANCES PAR NUIT" not in c:
    c += AMBIANCES
    modif = True
if modif:
    ecrire(f, c)
    print("✅ css/style.css")
else:
    print("⏭️  css/style.css déjà modifié")

print("\n🎉 Ambiances par nuit intégrées !")
print('git add . && git commit -m "🎨 Ambiances par nuit" && git push')