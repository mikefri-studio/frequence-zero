/* ============ DONNÉES — NUIT 3 « L'ANCIEN » ============ */
const NUIT3 = {
  titreNuit: "Nuit 3 — L'Ancien",
  intro: {
    titre: "2 h 34 — Studio B",
    texte: "Troisième nuit. Tu n'as pas dormi. Le rapport du standard est ouvert sur ton bureau : LIGNE 0, POSTE INTÉRIEUR, SOUS-SOL.\nLe voyant s'allume. Une voix que tu n'as jamais entendue."
  },
  auditeur: "L'Ancien",
  portrait: "assets/images/ancien.jpg",

  transcript: [
    { t: "00:02", qui: "???", texte: "Bonsoir. Vous ne me connaissez pas. Mais moi, je vous connais." },
    { t: "00:11", qui: "???", texte: "Je travaillais ici, il y a vingt ans. Avant l'incendie." },
    { t: "00:23", qui: "Toi", texte: "L'incendie du sous-sol ? Celui de la cabine ?" },
    { t: "00:28", qui: "???", texte: "Ce n'était pas un accident. Et Marco… Marco était là cette nuit-là." },
    { t: "00:41", qui: "???", texte: "Vous voulez une preuve ? J'ai retrouvé ce message, gravé sur la bande de l'époque." },
    { t: "00:52", qui: "???", texte: "« LOV RQW PLV OH IHX ». Décodez-le. Le nombre de rangs du décalage se cache dans votre première nuit." },
    { t: "01:08", qui: "???", texte: "Ensuite, comparez les deux enregistrements que je vous envoie. L'un est vrai. L'autre est un mensonge." },
    { t: "01:19", qui: "???", texte: "Je dois partir. Ils arrivent. Bonne chance." }
  ],

  enigmes: [
    {
      id: "cesar",
      titre: "1. Le message de l'incendie",
      question: "Décryptez : « LOV RQW PLV OH IHX ». Chaque lettre a été avancée de quelques rangs dans l'alphabet. Le nombre de rangs = le nombre d'énigmes de votre première nuit.",
      type: "saisie",
      reponse: ["ilsontmislefeu", "ils ont mis le feu"],
      indice: "Trois énigmes dans la Nuit 1 → reculez chaque lettre de 3 rangs : L→I, O→L, V→S…",
      note: "« ILS ONT MIS LE FEU ». Le message de la victime, gravé avant de mourir. L'incendie était criminel."
    },
    {
      id: "audio1",
      titre: "2. Enregistrement A — la nuit de l'incendie",
      question: "Écoutez, lisez le morse affiché, puis décodez : que crie la voix dans la cabine ?",
      type: "choix",
      boutonAudio: { texte: "🎧 Écouter l'enregistrement A", mot: "AIDEZMOI" },
      choix: [
        "« Partez, il arrive ! »",
        "« Aidez-moi, je suis coincé ! »",
        "« Le feu, le feu ! »",
        "« Je ne voulais pas… »"
      ],
      bonne: 1,
      indice: "Le début : ·− (A) ·· (I) −·· (D) · (E)…",
      note: "« AIDEZ-MOI » — quelqu'un était vivant dans la cabine pendant l'incendie."
    },
    {
      id: "audio2",
      titre: "3. Enregistrement B — le rapport officiel",
      question: "Maintenant, le rapport officiel de l'époque. Que dit-il ?",
      type: "choix",
      boutonAudio: { texte: "🎧 Écouter l'enregistrement B", mot: "PERSONNE" },
      choix: [
        "« Il n'y avait personne dans la cabine. »",
        "« Nous avons évacué tout le monde. »",
        "« L'incendie est accidentel. »",
        "« Le feu est parti du studio B. »"
      ],
      bonne: 0,
      indice: "Commence par ·−−· (P) et finit par · (E). Huit lettres.",
      note: "« PERSONNE » — le rapport mentait. Quelqu'un est mort dans cette cabine."
    },
    {
      id: "verite",
      titre: "4. La vérité",
      question: "Croisez tout : le message crypté, les deux enregistrements, les nuits 1 et 2. Que s'est-il vraiment passé ?",
      type: "choix",
      choix: [
        "L'incendie était accidentel, mais quelqu'un est mort par malchance.",
        "On a mis le feu pour tuer quelqu'un qui savait trop — et Marco était là.",
        "Marco a mis le feu par accident et il culpabilise.",
        "L'Ancien a survécu à l'incendie et se venge."
      ],
      bonne: 1,
      indice: "Pourquoi le rapport officiel ment-il sur la présence de quelqu'un ?",
      note: "Un meurtre déguisé en incendie. Marco était là cette nuit-là. Et il est revenu."
    }
  ],

  rappel: {
    question: "Tu rappelles L'Ancien. Il décroche à la première sonnerie. Que lui dis-tu ?",
    choix: [
      { texte: "« Qui est mort dans cette cabine ? »", bon: false,
        reaction: "Un long silence. « Pas encore. Vous n'êtes pas prêt. » Clic." },
      { texte: "« Marco a mis le feu pour tuer quelqu'un. Et il est revenu finir le travail. »", bon: true,
        reaction: "« Oui. Et il est en bas. EN CE MOMENT. Il sait que vous écoutez. »" },
      { texte: "« Pourquoi m'appelez-vous ? »", bon: false,
        reaction: "« Parce que vous êtes le seul à écouter vraiment. » Clic." }
    ]
  },

  fin: {
    crt: "APPEL : LIGNE 0\nORIGINE : POSTE INTÉRIEUR — SOUS-SOL\nHEURE : 2 h 47",
    texte: "L'Ancien avait raison. Marco est en bas.\nEt il sait que tu écoutes."
  }
};
