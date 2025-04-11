/**
 * Non-player characters (NPCs)
 * Each NPC has:
 * - id: Unique identifier
 * - name: NPC name (in Japanese and English)
 * - description: NPC description (in Japanese and English)
 * - dialogue: Possible dialogue options
 * - inventory: Items the NPC has
 * - targetVocabulary: Japanese words to learn from this NPC
 */

export const npcs = [
  {
    id: "old_man",
    name: {
      japanese: "お年寄り",
      romaji: "otoshiyori",
      english: "old man"
    },
    description: {
      japanese: "白い髪のお年寄りが椅子に座っています。",
      romaji: "Shiroi kami no otoshiyori ga isu ni suwatte imasu.",
      english: "An old man with white hair is sitting on a chair."
    },
    dialogue: {
      greeting: {
        japanese: "こんにちは！何かお手伝いしましょうか？",
        romaji: "Konnichiwa! Nanika otetsudai shimashou ka?",
        english: "Good day! How can I help you?"
      },
      responses: [
        {
          trigger: "ヘルプ",
          japanese: "ベッドルームのドアを開けるには鍵が必要です。",
          romaji: "Beddorūmu no doa o akeru ni wa kagi ga hitsuyoō desu.",
          english: "You need a key to open the door in the bedroom."
        },
        {
          trigger: "鍵",
          japanese: "鍵はスタートルームのテーブルの上にあります。",
          romaji: "Kagi wa sutāto rūmu no tēburu no ue ni arimasu.",
          english: "The key is on the table in the starting room."
        },
        {
          trigger: "本",
          japanese: "古い本には秘密があります。",
          romaji: "Furui hon ni wa himitsu ga arimasu.",
          english: "The old book contains a secret."
        },
        {
          trigger: "ありがとう",
          japanese: "どういたしまして！頑張ってください！",
          romaji: "Dō itashimashite! Ganbatte kudasai!",
          english: "You're welcome! Good luck!"
        }
      ]
    },
    inventory: [],
    targetVocabulary: ["お年寄り", "話す"]
  }
];

// Helper function to get an NPC by ID
export const getNpcById = (npcId) => {
  return npcs.find(npc => npc.id === npcId);
};

// Helper function to get an NPC's response based on a trigger word
export const getNpcResponse = (npcId, triggerWord) => {
  const npc = getNpcById(npcId);
  if (!npc || !npc.dialogue || !npc.dialogue.responses) return null;

  const response = npc.dialogue.responses.find(
    resp => resp.trigger.toLowerCase() === triggerWord.toLowerCase()
  );

  return response || null;
};
