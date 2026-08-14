/* ============ DONNÉES — NUIT 1 « MARCO » ============ */
const NUIT1 = {
  titreNuit: "Nuit 1 — Marco",
  intro: {
    titre: "23 h 58 — Studio B",
    texte: "La pluie frappe la vitre. Le néon « ON AIR » grésille au-dessus de la console.\nTu poses ton casque. Le standard affiche déjà un appel entrant."
  },
  auditeur: "Marco",
  portrait: "assets/images/marco.jpg",

  transcript: [
    { t: "00:03", qui: "Marco", texte: "Bonsoir… c'est Marco. Je suis sur la route." },
    { t: "00:11", qui: "Marco", texte: "Ça fait une heure qu'il pleut. Les essuie-glaces n'y suffisent pas, je vois à peine la route." },
    { t: "00:26", qui: "Toi",   texte: "Une nuit difficile, Marco. Vous êtes seul sur la route ?" },
    { t: "00:31", qui: "Marco", texte: "Je suis tout seul. Mais ça va… la pleine lune éclaire mon chemin." },
    { t: "00:58", qui: "Marco", texte: "Je… je dois vous laisser. Bonne nuit." },
    { t: "01:00", qui: "???",   texte: "niamed", murmure: true }
  ],

  enigmes: [
    {
      id: "contradiction",
      titre: "1. La contradiction",
      question: "Qu'est-ce qui ne colle pas dans le récit de Marco ?",
      type: "choix",
      choix: [
        "Il conduit trop vite sous la pluie.",
        "Une pluie battante… mais une pleine lune qui « éclaire la route ».",
        "Il appelle trop tard dans la nuit.",
        "Ses essuie-glaces sont trop bruyants."
      ],
      bonne: 1,
      indice: "Relis bien : sa météo décrit deux ciels différents.",
      note: "Par un tel déluge, aucune lune n'éclaire rien. Marco n'est PAS sur la route."
    },
    {
      id: "morse",
      titre: "2. Le morse du fond sonore",
      question: "En isolant l'ambiance, on entend un tapotement faible. Écoute-le et décode le mot.",
      type: "saisie",
      boutonMorse: true,
      oeufMorse: { texte: "🌀 Isoler la fréquence résiduelle", mot: "CABINE" },

      reponse: ["ici"],
      indice: "·· puis −·−· puis ··  →  I = ·· , C = −·−·",
      note: "Le morse disait « ICI ». L'auditeur « lointain » émet depuis ici."
    },
    {
      id: "murmure",
      titre: "3. Le murmure de fin",
      question: "Avant de raccrocher, une voix chuchote : « niamed ». Que veut-elle dire ?",
      type: "saisie",
      reponse: ["demain"],
      indice: "Certains messages s'écoutent… à l'envers.",
      note: "« niamed » à l'envers = « DEMAIN ». Il rappellera demain."
    }
  ],

  rappel: {
    question: "Marco décroche. Une seule question pour le faire craquer. Laquelle ?",
    choix: [
      { texte: "« Marco, pourquoi mentez-vous sur la météo ? »", bon: false,
        reaction: "Un long silence… puis un rire étouffé. « Vous n'y êtes pas. » Clic." },
      { texte: "« Marco… vous n'êtes pas sur la route. Vous êtes ICI, n'est-ce pas ? »", bon: true,
        reaction: "Silence. Une respiration proche, trop proche. « …vous m'avez entendu. À demain. »" },
      { texte: "« Marco, vous voulez simplement parler à quelqu'un ? »", bon: false,
        reaction: "« Non. Je voulais juste vérifier que vous écoutiez. » Clic." }
    ]
  },

  fin: {
    crt: "APPEL : LIGNE 0\nORIGINE : POSTE INTÉRIEUR",
    texte: "Le standard est formel : l'appel de Marco venait de l'intérieur du bâtiment.\nOr, tu es seul dans le studio."
  }
};