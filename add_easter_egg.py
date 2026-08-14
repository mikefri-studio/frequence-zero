# add_easter_egg.py — œuf de Pâques : la fréquence résiduelle « CABINE »
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

# --- game.js : lien discret après une énigme résolue (si oeufMorse) ---
PATCH_GAME = '''      if (en.oeufMorse) {
        const o = document.createElement("button");
        o.className = "lien"; o.textContent = en.oeufMorse.texte;
        o.onclick = () => { gresillement(2, 0.03); jouerMorse(en.oeufMorse.mot); afficherMorse(bloc, en.oeufMorse.mot); try { localStorage.setItem("fz-oeuf", en.oeufMorse.mot.toLowerCase()); } catch (e) {} };
        bloc.appendChild(o);
      }
'''

# --- nuit1.js : le morse caché sous le morse ---
OEUF_NUIT1 = '''      oeufMorse: { texte: "🌀 Isoler la fréquence résiduelle", mot: "CABINE" },
'''

# --- nuit2.js : la 4e énigme invisible ---
OEUF_NUIT2 = '''
/* ---------- ŒUF DE PÂQUES : fréquence résiduelle ---------- */
try {
  if ((localStorage.getItem("fz-oeuf") || "") === "cabine") {
    NUIT2.enigmes.push({
      id: "oeuf",
      titre: "4. La fréquence résiduelle",
      question: "Sous le témoignage de Sonia, la même fréquence résiduelle émet encore. Le mot décodé l'autre nuit n'était pas pour toi. Retape-le.",
      type: "saisie",
      boutonAudio: { texte: "🎧 Réécouter la fréquence résiduelle", mot: "CABINE" },
      reponse: ["cabine"],
      indice: "Six lettres. L'endroit où quelqu'un a brûlé, il y a vingt ans.",
      note: "CABINE. Le mot circulait déjà sur la ligne 0 avant l'incendie. Quelqu'un émet depuis la cabine. Toujours."
    });
  }
} catch (e) {}
'''

# --- 1. game.js ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
if "oeufMorse" in c:
    print("⏭️  js/game.js déjà modifié")
else:
    cible = "      bloc.appendChild(n);"
    if cible not in c:
        sys.exit("❌ Ligne bloc.appendChild(n) introuvable dans game.js")
    ecrire(f, c.replace(cible, cible + "\n" + PATCH_GAME, 1))
    print("✅ js/game.js")

# --- 2. nuit1.js ---
f = os.path.join(BASE, "js", "nuit1.js")
c = lire(f)
if "oeufMorse" in c:
    print("⏭️  js/nuit1.js déjà modifié")
else:
    cible = "      boutonMorse: true,"
    if cible not in c:
        sys.exit("❌ Ligne boutonMorse introuvable dans nuit1.js")
    ecrire(f, c.replace(cible, cible + "\n" + OEUF_NUIT1, 1))
    print("✅ js/nuit1.js")

# --- 3. nuit2.js ---
f = os.path.join(BASE, "js", "nuit2.js")
c = lire(f)
if "fz-oeuf" in c:
    print("⏭️  js/nuit2.js déjà modifié")
else:
    ecrire(f, c + OEUF_NUIT2)
    print("✅ js/nuit2.js")

print("\n🥚 Œuf de Pâques intégré !")
print('git add . && git commit -m "🥚 Easter egg : la fréquence résiduelle" && git push')