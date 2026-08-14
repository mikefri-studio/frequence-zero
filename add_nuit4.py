# add_nuit4.py — ajoute la Nuit 4 « La Ligne Zéro » + Marco spectral
import os, sys

BASE = "docs"

def lire(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()

def ecrire(f, c):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(c)

NUIT4_JS = r'''/* ============ DONNÉES — NUIT 4 « LA LIGNE ZÉRO » ============ */
const NUIT4 = {
  titreNuit: "Nuit 4 — La Ligne Zéro",
  intro: {
    titre: "3 h 33 — Studio B",
    texte: "Quatrième nuit. Tu n'as pas dormi. Sur le rapport, trois noms soulignés : MARCO, SONIA, L'ANCIEN.\nCe soir, le voyant LIGNE 0 ne s'allume pas. Il est déjà allumé.\nEt dans l'escalier de service, quelqu'un monte."
  },
  auditeur: "Marco",
  portrait: "assets/images/marco.jpg",
  portraitStyle: "grayscale(.75) contrast(1.25) brightness(.8)",

  transcript: [
    { t: "00:01", qui: "Marco", texte: "Vous avez décodé mon morse. Lu mes nuits. Vous êtes meilleur que les autres animateurs." },
    { t: "00:14", qui: "Marco", texte: "Il y a vingt ans, jour pour jour, cette station a brûlé une cabine. Avec quelqu'un dedans." },
    { t: "00:29", qui: "Toi",   texte: "Le 15 août. L'incendie a eu lieu un 15 août, c'est ça ?" },
    { t: "00:36", qui: "Marco", texte: "2006. J'y étais. J'ai fermé la porte. Je ne savais pas qu'il était encore dedans." },
    { t: "00:52", qui: "Marco", texte: "Vingt ans que j'appelle cette ligne. Vingt ans que personne n'écoute. Jusqu'à vous." },
    { t: "01:04", qui: "Marco", texte: "Je suis en bas de l'escalier. Une seule question : qu'est-ce que vous faites, maintenant ?" },
    { t: "01:15", qui: "???",   texte: "ervuo", murmure: true }
  ],

  enigmes: [
    {
      id: "annee",
      titre: "1. L'anniversaire",
      question: "Marco dit : « il y a vingt ans, jour pour jour ». Nous sommes le 15 août 2026. En quelle année la cabine a-t-elle brûlé ?",
      type: "saisie",
      reponse: ["2006"],
      indice: "2026 moins vingt ans, jour pour jour.",
      note: "15 août 2006. La nuit où la cabine a brûlé avec quelqu'un dedans. Marco n'a jamais oublié la date."
    },
    {
      id: "murmure4",
      titre: "2. Le murmure de la porte",
      question: "Avant de raccrocher, la ligne chuchote : « ervuo ». Que veut dire la voix ?",
      type: "saisie",
      reponse: ["ouvre", "ouvre la porte"],
      indice: "Comme la Nuit 1 : certains messages s'écoutent à l'envers.",
      note: "« ERVUO » à l'envers = « OUVRE ». Marco ne demande pas pardon. Il demande d'ouvrir."
    },
    {
      id: "morse4",
      titre: "3. La bande témoin",
      question: "Tu repasses la bande de 2006. Sous le crépitement, un morse faible. Décode-le : c'est le dernier mot de la victime.",
      type: "choix",
      boutonAudio: { texte: "🎧 Écouter la bande de 2006", mot: "PARDON" },
      choix: [
        "« Au secours. »",
        "« Pardon. »",
        "« Marco. »",
        "« Dehors. »"
      ],
      bonne: 1,
      indice: "·−−· (P) ·− (A) ·−· (R) −−− (O) −· (N)…",
      note: "« PARDON ». La victime savait qui fermait la porte. Et elle lui pardonnait déjà."
    },
    {
      id: "direct",
      titre: "4. La dernière émission",
      question: "Marco est derrière la porte. Ton micro est chaud. L'antenne attend. Que fais-tu ?",
      type: "choix",
      choix: [
        "Tu coupes l'antenne et tu te caches sous la console.",
        "Tu appelles la police et tu décris la porte qui tremble.",
        "Tu laisses le micro ouvert : « Confesse-toi. En direct. Comme elle t'a pardonné. »"
      ],
      bonne: 2,
      indice: "Tu es animateur. Ton arme, c'est l'antenne.",
      note: "Tu as laissé le micro ouvert. Vingt ans de silence ont fini en une confession, diffusée à 3 h 33."
    }
  ],

  rappel: {
    question: "La porte s'ouvre. Marco regarde le néon « ON AIR ». Il comprend que tout est enregistré. Que lui dis-tu ?",
    choix: [
      { texte: "« Elle t'a pardonné, Marco. Pas moi. »", bon: false,
        reaction: "Il recule d'un pas. « Alors pourquoi m'avoir laissé monter ? » Clic. Il disparaît dans l'escalier." },
      { texte: "« La bande tourne. Raconte la nuit du 15 août 2006. Pour elle. »", bon: true,
        reaction: "Un long silence. Puis une chaise. Une respiration. Et la voix de Marco, pour la première fois sans mensonge : « Il pleuvait, cette nuit-là… »" },
      { texte: "« Sors d'ici avant que j'appelle quelqu'un. »", bon: false,
        reaction: "« Personne ne viendra. La ligne 0 ne traverse pas les murs. » Il sourit. Clic." }
    ]
  },

  fin: {
    crt: "APPEL : LIGNE 0\nORIGINE : STUDIO B — MICRO OUVERT\nHEURE : 3 h 33",
    texte: "Le lendemain, la police a trouvé une bande qui tournait encore.\nDessus : une confession, un pardon, et le grésillement d'une ligne enfin muette.\nLa ligne 0 n'a plus jamais appelé."
  }
};
'''

FILTRE = '  $("#portrait").style.filter = nuit.portraitStyle || "";'

# --- 1. js/nuit4.js : crée ou complète ---
f = os.path.join(BASE, "js", "nuit4.js")
if os.path.exists(f):
    c = lire(f)
    if "portraitStyle" in c:
        print("⏭️  js/nuit4.js déjà complet")
    else:
        cible = '  portrait: "assets/images/marco.jpg",'
        if cible not in c:
            sys.exit("❌ Ligne portrait introuvable dans nuit4.js")
        ecrire(f, c.replace(cible, cible + '\n  portraitStyle: "grayscale(.75) contrast(1.25) brightness(.8)",', 1))
        print("✅ js/nuit4.js complété (portraitStyle)")
else:
    ecrire(f, NUIT4_JS)
    print("✅ js/nuit4.js créé")

# --- 2. index.html : charge nuit4.js avant game.js ---
f = os.path.join(BASE, "index.html")
html = lire(f)
if "nuit4.js" in html:
    print("⏭️  index.html déjà modifié")
else:
    cible = '<script src="js/game.js"></script>'
    if cible not in html:
        sys.exit("❌ Balise game.js introuvable dans index.html")
    ecrire(f, html.replace(cible, '<script src="js/nuit4.js"></script>\n' + cible, 1))
    print("✅ index.html")

# --- 3. game.js : tableau NUITS + filtre du portrait ---
f = os.path.join(BASE, "js", "game.js")
c = lire(f)
modif = False
if "NUIT4" not in c:
    cible = "const NUITS = [NUIT1, NUIT2, NUIT3];"
    if cible not in c:
        sys.exit("❌ Tableau NUITS introuvable dans game.js")
    c = c.replace(cible, "const NUITS = [NUIT1, NUIT2, NUIT3, NUIT4];", 1)
    modif = True
if "portraitStyle" not in c:
    cible = '  $("#portrait").src = nuit.portrait;'
    if cible not in c:
        sys.exit("❌ Ligne portrait introuvable dans game.js")
    c = c.replace(cible, cible + '\n' + FILTRE, 1)
    modif = True
if modif:
    ecrire(f, c)
    print("✅ js/game.js")
else:
    print("⏭️  js/game.js déjà modifié")

# --- 4. vérifie le portrait ---
p = os.path.join(BASE, "assets", "images", "marco.jpg")
print(("✅ " if os.path.exists(p) else "⚠️  MANQUANT : ") + p)

print("\n🎉 Nuit 4 intégrée ! Teste, puis :")
print('git add . && git commit -m "🌙 Nuit 4 — La Ligne Zéro + Marco spectral" && git push')