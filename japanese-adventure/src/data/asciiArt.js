/**
 * ASCII art for rooms, items, and NPCs
 */

const asciiArt = {
  // Room ASCII art
  rooms: {
    // Starting room
    start: `
    +----------------+
    |                |
    |   +---------+  |
    |   |  テーブル |  |
    |   +---------+  |
    |                |
    |                |
    |       ^        |
    |       |        |
    +-------+--------+
            ドア
    `,

    // Living room
    living_room: `
    +----------------+
    |                |
    |  +-+           |
    |  |お|    +---+  |
    |  +-+    |   |  |
    |         +---+  |
    |  椅子         |
    |                |
    |                |
    +-------+---+----+
            |   |
            +---+
    `,

    // Kitchen
    kitchen: `
    +----------------+
    |                |
    |  +----------+  |
    |  |          |  |
    |  |  冷蔵庫  |  |
    |  +----------+  |
    |                |
    |   +---------+  |
    |   | テーブル |  |
    +---+---------+--+
    `,

    // Bedroom
    bedroom: `
    +----------------+
    |                |
    |  +----------+  |
    |  |          |  |
    |  |  ベッド   |  |
    |  |          |  |
    |  +----------+  |
    |                |
    |           +--+ |
    +-----------+--+-+
                 ドア
    `,

    // Secret room
    locked_room: `
    +----------------+
    |                |
    |   +---------+  |
    |   | テーブル |  |
    |   | +-----+ |  |
    |   | | 本  | |  |
    |   | +-----+ |  |
    |   +---------+  |
    |                |
    +----------------+
    `,

    // Default room (fallback)
    default: `
    +----------------+
    |                |
    |                |
    |                |
    |                |
    |                |
    |                |
    |                |
    |                |
    +----------------+
    `
  },

  // Item ASCII art
  items: {
    // Key
    key: `
  .---.
 /    |
[     |
 \\___/
    `,

    // Book
    book: `
  +---------+
  |   本    |
  |         |
  +---------+
    `,

    // Old book
    old_book: `
  +---------+
  | 古い    |
  |  本    |
  +---------+
    `,

    // Chair
    chair: `
    +-+
    | |
  +-+ +-+
  |     |
  +-----+
    `,

    // Bread
    bread: `
   (     )
    '---'
    `,

    // Water
    water: `
    _____
   |     |
   | 水  |
   |_____|
    `,

    // Note
    note: `
  +-------+
  | メモ  |
  +-------+
    `,

    // Default item (fallback)
    default: `
    [?]
    `
  },

  // NPC ASCII art
  npcs: {
    // Old man
    old_man: `
     ,---,
    (o   o)
     \\ ~ /
    お年寄り
    `,

    // Default NPC (fallback)
    default: `
     ,---,
    (     )
     \\___/
    `
  }
};

export default asciiArt;
