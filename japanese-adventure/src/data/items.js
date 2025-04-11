/**
 * Game items
 * Each item has:
 * - id: Unique identifier
 * - name: Item name (in Japanese and English)
 * - description: Item description (in Japanese and English)
 * - canTake: Whether the item can be picked up
 * - canUse: Whether the item can be used
 * - canOpen: Whether the item can be opened
 * - isContainer: Whether the item can contain other items
 * - containedItems: Items contained within this item
 * - targetVocabulary: Japanese words to learn with this item
 */

export const items = [
  {
    id: "key",
    name: {
      japanese: "鍵",
      romaji: "kagi",
      english: "key"
    },
    description: {
      japanese: "小さい金属の鍵です。",
      romaji: "Chiisai kinzoku no kagi desu.",
      english: "A small metal key."
    },
    canTake: true,
    canUse: true,
    canOpen: false,
    isContainer: false,
    containedItems: [],
    targetVocabulary: ["鍵", "小さい"]
  },
  {
    id: "book",
    name: {
      japanese: "本",
      romaji: "hon",
      english: "book"
    },
    description: {
      japanese: "日本語についての新しい本です。",
      romaji: "Nihongo ni tsuite no atarashii hon desu.",
      english: "A new book about the Japanese language."
    },
    canTake: true,
    canUse: true,
    canOpen: true,
    isContainer: false,
    containedItems: [],
    targetVocabulary: ["本", "新しい"]
  },
  {
    id: "chair",
    name: {
      japanese: "椅子",
      romaji: "isu",
      english: "chair"
    },
    description: {
      japanese: "大きくて快適な椅子です。",
      romaji: "Ōkikute kaitekina isu desu.",
      english: "A big, comfortable chair."
    },
    canTake: false,
    canUse: true,
    canOpen: false,
    isContainer: false,
    containedItems: [],
    targetVocabulary: ["椅子", "大きい"]
  },
  {
    id: "bread",
    name: {
      japanese: "パン",
      romaji: "pan",
      english: "bread"
    },
    description: {
      japanese: "新鮮で美味しいパンです。",
      romaji: "Shinsen de oishii pan desu.",
      english: "A fresh, delicious bread."
    },
    canTake: true,
    canUse: false,
    canOpen: false,
    isContainer: false,
    containedItems: [],
    targetVocabulary: ["パン"]
  },
  {
    id: "water",
    name: {
      japanese: "水",
      romaji: "mizu",
      english: "water"
    },
    description: {
      japanese: "冷たい水の入ったグラスです。",
      romaji: "Tsumetai mizu no haitta gurasu desu.",
      english: "A glass of cold water."
    },
    canTake: true,
    canUse: false,
    canOpen: false,
    isContainer: false,
    containedItems: [],
    targetVocabulary: ["水"]
  },
  {
    id: "old_book",
    name: {
      japanese: "古い本",
      romaji: "furui hon",
      english: "old book"
    },
    description: {
      japanese: "日本の物語が書かれた古くて埃っぽい本です。",
      romaji: "Nihon no monogatari ga kakareta furukute hokori-ppoi hon desu.",
      english: "An old, dusty book with Japanese stories."
    },
    canTake: true,
    canUse: true,
    canOpen: true,
    isContainer: true,
    containedItems: ["note"],
    targetVocabulary: ["本", "古い"]
  },
  {
    id: "note",
    name: {
      japanese: "メモ",
      romaji: "memo",
      english: "note"
    },
    description: {
      japanese: "日本語で書かれたメモ：「おめでとう！秘密を見つけました！」",
      romaji: "Nihongo de kakareta memo: 'Omedetou! Himitsu o mitsukemashita!'",
      english: "A note written in Japanese: 'Congratulations! You found the secret!'"
    },
    canTake: true,
    canUse: true,
    canOpen: false,
    isContainer: false,
    containedItems: [],
    targetVocabulary: ["メモ", "秘密"]
  }
];

// Helper function to get an item by ID
export const getItemById = (itemId) => {
  return items.find(item => item.id === itemId);
};

// Helper function to get an item by its Japanese name
export const getItemByJapaneseName = (japaneseName) => {
  return items.find(item =>
    item.name.japanese === japaneseName ||
    item.name.romaji.toLowerCase() === japaneseName.toLowerCase()
  );
};
