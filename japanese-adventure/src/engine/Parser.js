/**
 * Command parser for the Japanese language immersion game
 * Parses user input and converts it to structured commands
 */

// Define command patterns for both Japanese and English
const commandPatterns = {
  // Look command
  look: {
    english: [
      { regex: /^look$/i, action: 'look' },
      { regex: /^look at (.+)$/i, action: 'look', objectGroup: 1 },
      { regex: /^examine (.+)$/i, action: 'look', objectGroup: 1 },
      { regex: /^inspect (.+)$/i, action: 'look', objectGroup: 1 }
    ],
    japanese: [
      { regex: /^(見る|みる|見て|みて|miru|mite)$/i, action: 'look' },
      { regex: /^(見る|みる|見て|みて|miru|mite)(を|o)?(.+)$/i, action: 'look', objectGroup: 3 },
      { regex: /^(.+)(を|o)(見る|みる|見て|みて|miru|mite)$/i, action: 'look', objectGroup: 1 }
    ]
  },

  // Move command
  move: {
    english: [
      { regex: /^(go|move) (north|south|east|west|up|down|left|right)$/i, action: 'move', directionGroup: 2 },
      { regex: /^(north|south|east|west|up|down|left|right)$/i, action: 'move', directionGroup: 1 }
    ],
    japanese: [
      { regex: /^(行く|いく|移動|いどう|iku|idou)(へ|に|he|ni)?(北|きた|南|みなみ|東|ひがし|西|にし|上|うえ|下|した|左|ひだり|右|みぎ|kita|minami|higashi|nishi|ue|shita|hidari|migi)$/i, action: 'move', directionGroup: 3 },
      { regex: /^(北|きた|南|みなみ|東|ひがし|西|にし|上|うえ|下|した|左|ひだり|右|みぎ|kita|minami|higashi|nishi|ue|shita|hidari|migi)(へ|に|he|ni)?(行く|いく|iku)?$/i, action: 'move', directionGroup: 1 }
    ]
  },

  // Take command
  take: {
    english: [
      { regex: /^(take|pick up|grab|get) (.+)$/i, action: 'take', objectGroup: 2 }
    ],
    japanese: [
      { regex: /^(取る|とる|toru)(.+)$/i, action: 'take', objectGroup: 2 },
      { regex: /^(.+)(を|o)(取る|とる|toru)$/i, action: 'take', objectGroup: 1 }
    ]
  },

  // Drop command
  drop: {
    english: [
      { regex: /^(drop|put down|discard) (.+)$/i, action: 'drop', objectGroup: 2 }
    ],
    japanese: [
      { regex: /^(置く|おく|落とす|おとす|oku|otosu)(.+)$/i, action: 'drop', objectGroup: 2 },
      { regex: /^(.+)(を|o)(置く|おく|落とす|おとす|oku|otosu)$/i, action: 'drop', objectGroup: 1 }
    ]
  },

  // Inventory command
  inventory: {
    english: [
      { regex: /^(inventory|items|i)$/i, action: 'inventory' }
    ],
    japanese: [
      { regex: /^(持ち物|もちもの|インベントリ|アイテム|mochimono|inbentori|aitemu|i)$/i, action: 'inventory' }
    ]
  },

  // Use command
  use: {
    english: [
      { regex: /^(use|utilize) (.+)$/i, action: 'use', objectGroup: 2 },
      { regex: /^(use|utilize) (.+) (on|with) (.+)$/i, action: 'use', objectGroup: 2, targetGroup: 4 }
    ],
    japanese: [
      { regex: /^(使う|つかう|tsukau)(.+)$/i, action: 'use', objectGroup: 2 },
      { regex: /^(.+)(を|o)(使う|つかう|tsukau)$/i, action: 'use', objectGroup: 1 },
      { regex: /^(.+)(を|o)(.+)(に|で|ni|de)(使う|つかう|tsukau)$/i, action: 'use', objectGroup: 1, targetGroup: 3 }
    ]
  },

  // Open command
  open: {
    english: [
      { regex: /^open (.+)$/i, action: 'open', objectGroup: 1 }
    ],
    japanese: [
      { regex: /^(開ける|あける|akeru)(.+)$/i, action: 'open', objectGroup: 2 },
      { regex: /^(.+)(を|o)(開ける|あける|akeru)$/i, action: 'open', objectGroup: 1 }
    ]
  },

  // Close command
  close: {
    english: [
      { regex: /^(close|shut) (.+)$/i, action: 'close', objectGroup: 2 }
    ],
    japanese: [
      { regex: /^(閉める|しめる|shimeru)(.+)$/i, action: 'close', objectGroup: 2 },
      { regex: /^(.+)(を|o)(閉める|しめる|shimeru)$/i, action: 'close', objectGroup: 1 }
    ]
  },

  // Eat command
  eat: {
    english: [
      { regex: /^(eat|consume) (.+)$/i, action: 'eat', objectGroup: 2 }
    ],
    japanese: [
      { regex: /^(食べる|たべる|taberu)(.+)$/i, action: 'eat', objectGroup: 2 },
      { regex: /^(.+)(を|o)(食べる|たべる|taberu)$/i, action: 'eat', objectGroup: 1 }
    ]
  },

  // Drink command
  drink: {
    english: [
      { regex: /^(drink|sip) (.+)$/i, action: 'drink', objectGroup: 2 }
    ],
    japanese: [
      { regex: /^(飲む|のむ|nomu)(.+)$/i, action: 'drink', objectGroup: 2 },
      { regex: /^(.+)(を|o)(飲む|のむ|nomu)$/i, action: 'drink', objectGroup: 1 }
    ]
  },

  // Talk command
  talk: {
    english: [
      { regex: /^(talk|speak) (to|with) (.+)$/i, action: 'talk', objectGroup: 3 }
    ],
    japanese: [
      { regex: /^(話す|はなす|hanasu)(.+)(と|に|to|ni)$/i, action: 'talk', objectGroup: 2 },
      { regex: /^(.+)(と|に|to|ni)(話す|はなす|hanasu)$/i, action: 'talk', objectGroup: 1 }
    ]
  },

  // Say command
  say: {
    english: [
      { regex: /^(say|tell) (.+) (to) (.+)$/i, action: 'say', objectGroup: 2, targetGroup: 4 }
    ],
    japanese: [
      { regex: /^(言う|いう|iu)(.+)(を|o)(.+)(に|ni)$/i, action: 'say', objectGroup: 2, targetGroup: 4 },
      { regex: /^(.+)(に|ni)(.+)(と|to)(言う|いう|iu)$/i, action: 'say', objectGroup: 3, targetGroup: 1 }
    ]
  },

  // Give command
  give: {
    english: [
      { regex: /^(give|hand) (.+) (to) (.+)$/i, action: 'give', objectGroup: 2, targetGroup: 4 }
    ],
    japanese: [
      { regex: /^(あげる|渡す|わたす|ageru|watasu)(.+)(を|o)(.+)(に|ni)$/i, action: 'give', objectGroup: 2, targetGroup: 4 },
      { regex: /^(.+)(に|ni)(.+)(を|o)(あげる|渡す|わたす|ageru|watasu)$/i, action: 'give', objectGroup: 3, targetGroup: 1 }
    ]
  },

  // Help command
  help: {
    english: [
      { regex: /^(help|commands|instructions)$/i, action: 'help' }
    ],
    japanese: [
      { regex: /.*(ヘルプ|へるぷ|herupu|助け|たすけ|コマンド|命令|めいれい|コマンド一覧|コマンドリスト).*/i, action: 'help' }
    ]
  }
};

// Direction mappings
const directionMappings = {
  // English
  'north': 'north',
  'south': 'south',
  'east': 'east',
  'west': 'west',
  'up': 'up',
  'down': 'down',
  'left': 'left',
  'right': 'right',

  // Japanese
  '北': 'north',
  'きた': 'north',
  '南': 'south',
  'みなみ': 'south',
  '東': 'east',
  'ひがし': 'east',
  '西': 'west',
  'にし': 'west',
  '上': 'up',
  'うえ': 'up',
  '下': 'down',
  'した': 'down',
  '左': 'left',
  'ひだり': 'left',
  '右': 'right',
  'みぎ': 'right'
};

/**
 * Parse a command string and return a structured command object
 * @param {string} commandString - The command string to parse
 * @returns {Object|null} - The parsed command or null if not recognized
 */
export const parseCommand = (commandString) => {
  if (!commandString || typeof commandString !== 'string') {
    return null;
  }

  // Trim the command string
  const trimmedCommand = commandString.trim();

  // Debug: Log the command and its character codes
  console.log('Command:', trimmedCommand);
  console.log('Character codes:', Array.from(trimmedCommand).map(c => c.charCodeAt(0)));

  // Special case for ヘルプ (herupu)
  if (trimmedCommand === 'ヘルプ' ||
      trimmedCommand.toLowerCase() === 'herupu' ||
      trimmedCommand === 'へるぷ' ||
      trimmedCommand.toLowerCase() === 'h' ||
      trimmedCommand.toLowerCase() === 'help') {
    console.log('Help command detected!');
    return { action: 'help' };
  }

  // Try to match the command against all patterns
  for (const [commandType, languages] of Object.entries(commandPatterns)) {
    // Try both English and Japanese patterns
    for (const [language, patterns] of Object.entries(languages)) {
      for (const pattern of patterns) {
        const match = trimmedCommand.match(pattern.regex);

        if (match) {
          const command = {
            action: pattern.action
          };

          // Add direction if applicable
          if (pattern.directionGroup !== undefined && match[pattern.directionGroup]) {
            const directionInput = match[pattern.directionGroup].toLowerCase();
            command.direction = directionMappings[directionInput] || directionInput;
          }

          // Add object if applicable
          if (pattern.objectGroup !== undefined && match[pattern.objectGroup]) {
            command.object = match[pattern.objectGroup].toLowerCase();
          }

          // Add target if applicable
          if (pattern.targetGroup !== undefined && match[pattern.targetGroup]) {
            command.target = match[pattern.targetGroup].toLowerCase();
          }

          return command;
        }
      }
    }
  }

  // No match found
  return null;
};
