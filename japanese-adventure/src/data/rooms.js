/**
 * Game rooms and locations
 * Each room has:
 * - id: Unique identifier
 * - name: Room name (in Japanese and English)
 * - description: Room description (in Japanese and English)
 * - exits: Available exits to other rooms
 * - items: Items in the room
 * - npcs: NPCs in the room
 * - targetVocabulary: Japanese words to learn in this room
 */

export const rooms = [
  {
    id: "start",
    name: {
      japanese: "スタートルーム",
      romaji: "Sutāto rūmu",
      english: "Starting Room"
    },
    description: {
      japanese: "あなたは白い壁の小さな部屋にいます。真ん中にテーブルがあり、北にドアがあります。",
      romaji: "Anata wa shiroi kabe no chiisana heya ni imasu. Mannaka ni tēburu ga ari, kita ni doa ga arimasu.",
      english: "You are in a small room with white walls. There is a table in the middle and a door to the north."
    },
    exits: {
      north: "living_room"
    },
    items: ["key", "book"],
    npcs: [],
    targetVocabulary: ["テーブル", "ドア"]
  },
  {
    id: "living_room",
    name: {
      japanese: "リビングルーム",
      romaji: "Ribingu rūmu",
      english: "Living Room"
    },
    description: {
      japanese: "あなたはリビングルームにいます。大きい椅子と窓があります。南か東に行くことができます。",
      romaji: "Anata wa ribingu rūmu ni imasu. Ōkii isu to mado ga arimasu. Minami ka higashi ni iku koto ga dekimasu.",
      english: "You are in the living room. There is a big chair and a window. You can go south or east."
    },
    exits: {
      south: "start",
      east: "kitchen"
    },
    items: ["chair"],
    npcs: ["old_man"],
    targetVocabulary: ["椅子", "窓", "大きい"]
  },
  {
    id: "kitchen",
    name: {
      japanese: "キッチン",
      romaji: "Kicchin",
      english: "Kitchen"
    },
    description: {
      japanese: "あなたはキッチンにいます。小さいテーブルと冷蔵庫があります。西か北に行くことができます。",
      romaji: "Anata wa kicchin ni imasu. Chiisai tēburu to reizōko ga arimasu. Nishi ka kita ni iku koto ga dekimasu.",
      english: "You are in the kitchen. There is a small table and a refrigerator. You can go west or north."
    },
    exits: {
      west: "living_room",
      north: "bedroom"
    },
    items: ["bread", "water"],
    npcs: [],
    targetVocabulary: ["パン", "水", "小さい"]
  },
  {
    id: "bedroom",
    name: {
      japanese: "ベッドルーム",
      romaji: "Beddorūmu",
      english: "Bedroom"
    },
    description: {
      japanese: "あなたはベッドルームにいます。大きいベッドと東に閉まったドアがあります。",
      romaji: "Anata wa beddorūmu ni imasu. Ōkii beddo to higashi ni shimatta doa ga arimasu.",
      english: "You are in the bedroom. There is a big bed and a closed door to the east."
    },
    exits: {
      south: "kitchen",
      east: "locked_room" // This door is locked and requires a key
    },
    items: [],
    npcs: [],
    targetVocabulary: ["ベッド", "閉まった"]
  },
  {
    id: "locked_room",
    name: {
      japanese: "秘密の部屋",
      romaji: "Himitsu no heya",
      english: "Secret Room"
    },
    description: {
      japanese: "あなたは秘密の部屋にいます。テーブルの上に古い本があります。",
      romaji: "Anata wa himitsu no heya ni imasu. Tēburu no ue ni furui hon ga arimasu.",
      english: "You are in a secret room. There is an old book on a table."
    },
    exits: {
      west: "bedroom"
    },
    items: ["old_book"],
    npcs: [],
    targetVocabulary: ["秘密", "古い"]
  }
];

// Helper function to get a room by ID
export const getRoomById = (roomId) => {
  return rooms.find(room => room.id === roomId);
};

// Helper function to get available exits from a room
export const getAvailableExits = (roomId) => {
  const room = getRoomById(roomId);
  if (!room) return [];

  return Object.entries(room.exits).map(([direction, targetRoomId]) => ({
    direction,
    targetRoomId
  }));
};
