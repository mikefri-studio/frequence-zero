/* ============ DONNÉES — NUIT 5 « LA FRÉQUENCE MORTE » ============ */
const NUIT5 = {
  titreNuit: "Nuit 5 — La Fréquence Morte",
  intro: {
    titre: "4 h 00 — Le standard muet",
    texte: "Le voyant clignote. Pas de numéro. Juste un grésillement continu, épais comme de l'eau noire.\nTu décroches. La voix ne vient pas du combiné. Elle semble venir des enceintes de contrôle, des murs, de ta propre respiration."
  },
  auditeur: "Sonia",
  portrait: "assets/images/sonia.jpg",
  portraitStyle: "sepia(0.8) contrast(1.4) brightness(0.7) blur(0.5px)",

  transcript: [
    { t: "00:00", qui: "???", texte: "...zzzt... vous m'entendez enfin ?" },
    { t: "00:08", qui: "Toi", texte: "Qui est à l'appareil ? Le numéro ne s'affiche pas." },
    { t: "00:14", qui: "Sonia", texte: "Marco a parlé. Il a dit la moitié de la vérité. La moitié confortable." },
    { t: "00:23", qui: "Sonia", texte: "Il n'a pas fermé la porte par erreur. Il a obéi. L'Ancien a verrouillé la cabine." },
    { t: "00:35", qui: "Toi", texte: "Pourquoi me dire ça maintenant ? Vingt ans après." },
    { t: "00:42", qui: "Sonia", texte: "Parce que j'ai caché la bande témoin dans le bruit. Dans la fréquence morte. Écoutez." },
    { t: "00:50", qui: "???", texte: "netnel neicna'l", murmure: true }
  ],

  enigmes: [
    {
      id: "frequence",
      titre: "1. La Fréquence Porteuse",
      question: "Le son est noyé sous les parasites. L'indice de Sonia mentionne 'la fréquence des esprits, un demi-ton au-dessus du La standard'. (Indice : 415 Hz). Quelle fréquence dois-tu régler ?",
      type: "saisie",
      reponse: ["415", "415hz", "415 hz"],
      indice: "Un demi-ton au-dessus de 440 Hz, c'est environ 415 Hz dans l'échelle des fréquences fantômes.",
      note: "415 Hz. Le bruit blanc s'écarte. La voix devient claire."
    },
    {
      id: "murmure5",
      titre: "2. Le Murmure à l'envers",
      question: "À 415 Hz, le murmure est net : « netnel neicna'l ». Que dit vraiment la voix ?",
      type: "saisie",
      reponse: ["l'ancien ment", "lancien ment"],
      indice: "Comme en Nuit 1 et 4, lisez le message à l'envers.",
      note: "« L'ANCIEN MENT ». La pièce se fige. Vous entendez des pas dans le couloir."
    },
    {
      id: "choix_final",
      titre: "3. Le Direct",
      question: "La poignée de la porte du studio tourne. L'Ancien est là. La bande tourne. Que fais-tu ?",
      type: "choix",
      choix: [
        "Tu coupes le micro et tu caches la bande sous la console.",
        "Tu appelles la police en chuchotant, en coupant l'antenne.",
        "Tu pousses le fader principal à fond : « Ici Fréquence Zéro. Voici la vérité. »"
      ],
      bonne: 2,
      indice: "Tu es animateur. Ton arme, c'est l'antenne. Ne la laisse pas se taire une seconde fois.",
      note: "Le fader est au maximum. Le voyant ON AIR brûle d'un rouge vif. La porte s'ouvre, mais il est trop tard. La ville entière écoute."
    }
  ],

  rappel: {
    question: "L'Ancien est dans l'encadrement de la porte. Il voit le voyant rouge. Il voit la bande. Que lui dis-tu en direct ?",
    choix: [
      { texte: "« C'est fini. Écoutez ce qu'elle a à dire. »", bon: true,
        reaction: "Il pâlit. Ses mains tremblent. Il ne dit rien, se retourne et s'effondre dans le couloir. La vérité est en ondes." },
      { texte: "« Vous pouvez encore arrêter ça. Coupez le courant. »", bon: false,
        reaction: "Il sourit tristement. « C'est ce que j'ai fait en 2006. Ça n'a pas marché. » Il coupe le micro. Silence." }
    ]
  },

  fin: {
    crt: "APPEL : LIGNE 0\nORIGINE : INCONNUE\nHEURE : 4 h 17\nSTATUT : DIFFUSION NATIONALE EN COURS",
    texte: "La station a fermé définitivement le lendemain.\nMais la bande a circulé. Sur des cassettes, des forums, des ondes courtes.\nQuelque part, à 4h00 du matin, si vous tendez l'oreille entre deux stations...\nVous l'entendrez encore."
  }
};
