import { getRoomById } from '../data/rooms';
import { getItemById } from '../data/items';
import { getNpcById, getNpcResponse } from '../data/npcs';
import { findWordByJapanese, findWordByEnglish } from '../data/vocabulary';
import { parseCommand } from './Parser';

class GameEngine {
  constructor() {
    this.gameState = {
      currentRoomId: 'start',
      inventory: [],
      visitedRooms: new Set(['start']),
      learnedVocabulary: new Set(),
      gameLog: [],
      gameOver: false
    };
  }

  // Initialize or reset the game
  initGame() {
    this.gameState = {
      currentRoomId: 'start',
      inventory: [],
      visitedRooms: new Set(['start']),
      learnedVocabulary: new Set(),
      gameLog: [],
      gameOver: false
    };

    // Add initial game message
    this.addToGameLog({
      japanese: 'ようこそ日本語アドベンチャーへ！コマンドについては「ヘルプ」と入力してください。',
      romaji: 'Yōkoso Nihongo Adobenchā e! Komando ni tsuite wa "herupu" to nyūryoku shite kudasai.',
      english: 'Welcome to the Japanese Adventure! Type "help" for commands.'
    });

    // Add the current room description
    this.describeCurrentRoom();

    return this.gameState;
  }

  // Process a user command
  processCommand(commandText) {
    // Special case for help command
    if (commandText === 'ヘルプ' ||
        commandText.toLowerCase() === 'herupu' ||
        commandText === 'へるぷ' ||
        commandText.toLowerCase() === 'h' ||
        commandText.toLowerCase() === 'help') {
      this.showHelp();
      return this.gameState;
    }

    // Parse the command
    const command = parseCommand(commandText);

    if (!command) {
      this.addToGameLog({
        japanese: 'そのコマンドは理解できません。もう一度お試しください。',
        romaji: 'Sono komando wa rikai dekimasen. Mō ichido o-tameshi kudasai.',
        english: 'I don\'t understand that command. Try again.'
      });
      return this.gameState;
    }

    // Process the command based on the action
    switch (command.action) {
      case 'help':
        this.showHelp();
        break;
      case 'look':
        if (command.object) {
          this.lookAtObject(command.object);
        } else {
          this.describeCurrentRoom();
        }
        break;
      case 'move':
        this.moveToDirection(command.direction);
        break;
      case 'take':
        this.takeItem(command.object);
        break;
      case 'drop':
        this.dropItem(command.object);
        break;
      case 'inventory':
        this.showInventory();
        break;
      case 'use':
        this.useItem(command.object, command.target);
        break;
      case 'open':
        this.openObject(command.object);
        break;
      case 'close':
        this.closeObject(command.object);
        break;
      case 'eat':
        this.eatItem(command.object);
        break;
      case 'drink':
        this.drinkItem(command.object);
        break;
      case 'talk':
        this.talkToNpc(command.object);
        break;
      case 'say':
        this.sayToNpc(command.object, command.target);
        break;
      case 'give':
        this.giveItemToNpc(command.object, command.target);
        break;
      default:
        this.addToGameLog({
          japanese: 'そのコマンドは理解できません。もう一度お試しください。',
          romaji: 'Sono komando wa rikai dekimasen. Mō ichido o-tameshi kudasai.',
          english: 'I don\'t understand that command. Try again.'
        });
    }

    return this.gameState;
  }

  // Add a message to the game log
  addToGameLog(message) {
    this.gameState.gameLog.push({
      id: Date.now(),
      message
    });
  }

  // Get the current room
  getCurrentRoom() {
    return getRoomById(this.gameState.currentRoomId);
  }

  // Describe the current room
  describeCurrentRoom() {
    const room = this.getCurrentRoom();

    if (!room) {
      this.addToGameLog({
        japanese: 'エラー：部屋が存在しません。',
        romaji: 'Erā: Heya ga sonzai shimasen.',
        english: 'Error: Room does not exist.'
      });
      return;
    }

    // Add room name and description to the game log
    this.addToGameLog({
      japanese: `${room.name.japanese}`,
      romaji: `${room.name.romaji}`,
      english: `${room.name.english}`
    });

    this.addToGameLog({
      japanese: room.description.japanese,
      romaji: room.description.romaji,
      english: room.description.english
    });

    // Describe items in the room
    if (room.items && room.items.length > 0) {
      const japaneseItems = room.items.map(itemId => {
        const item = getItemById(itemId);
        return item ? item.name.japanese : '';
      }).filter(Boolean);

      const romajiItems = room.items.map(itemId => {
        const item = getItemById(itemId);
        return item ? item.name.romaji : '';
      }).filter(Boolean);

      const englishItems = room.items.map(itemId => {
        const item = getItemById(itemId);
        return item ? item.name.english : '';
      }).filter(Boolean);

      if (japaneseItems.length > 0) {
        this.addToGameLog({
          japanese: `見えるもの：${japaneseItems.join(', ')}。`,
          romaji: `Mieru mono: ${romajiItems.join(', ')}.`,
          english: `You see: ${englishItems.join(', ')}.`
        });
      }
    }

    // Describe NPCs in the room
    if (room.npcs && room.npcs.length > 0) {
      const japaneseNpcs = room.npcs.map(npcId => {
        const npc = getNpcById(npcId);
        return npc ? npc.name.japanese : '';
      }).filter(Boolean);

      const romajiNpcs = room.npcs.map(npcId => {
        const npc = getNpcById(npcId);
        return npc ? npc.name.romaji : '';
      }).filter(Boolean);

      const englishNpcs = room.npcs.map(npcId => {
        const npc = getNpcById(npcId);
        return npc ? npc.name.english : '';
      }).filter(Boolean);

      if (japaneseNpcs.length > 0) {
        this.addToGameLog({
          japanese: `人：${japaneseNpcs.join(', ')}。`,
          romaji: `Hito: ${romajiNpcs.join(', ')}.`,
          english: `People: ${englishNpcs.join(', ')}.`
        });
      }
    }

    // Describe exits
    const exits = Object.keys(room.exits);
    if (exits.length > 0) {
      // Map directions to Japanese
      const directionMap = {
        'north': '北',
        'south': '南',
        'east': '東',
        'west': '西',
        'up': '上',
        'down': '下'
      };

      // Map directions to romaji
      const romajiDirectionMap = {
        'north': 'kita',
        'south': 'minami',
        'east': 'higashi',
        'west': 'nishi',
        'up': 'ue',
        'down': 'shita'
      };

      // Create Japanese and romaji exit lists
      const japaneseExits = exits.map(exit => directionMap[exit] || exit);
      const romajiExits = exits.map(exit => romajiDirectionMap[exit] || exit);

      this.addToGameLog({
        japanese: `出口：${japaneseExits.join(', ')}。`,
        romaji: `Deguchi: ${romajiExits.join(', ')}.`,
        english: `Exits: ${exits.join(', ')}.`
      });
    }

    // Learn vocabulary from this room
    if (room.targetVocabulary) {
      room.targetVocabulary.forEach(word => {
        this.gameState.learnedVocabulary.add(word);
      });
    }
  }

  // Show help
  showHelp() {
    this.addToGameLog({
      japanese: '利用可能なコマンド：',
      romaji: 'Riyō kanō na komando:',
      english: 'Available commands:'
    });

    const commands = [
      { japanese: '見る / 見る', romaji: 'miru / miru', english: 'look' },
      { japanese: '行く [方向]', romaji: 'iku [hōkō]', english: 'move [direction]' },
      { japanese: '北 / 南 / 東 / 西', romaji: 'kita / minami / higashi / nishi', english: 'north / south / east / west' },
      { japanese: '取る [物]', romaji: 'toru [mono]', english: 'take [object]' },
      { japanese: '置く [物]', romaji: 'oku [mono]', english: 'drop [object]' },
      { japanese: '[人]と話す', romaji: '[hito] to hanasu', english: 'talk to [person]' },
      { japanese: '[人]に[言葉]と言う', romaji: '[hito] ni [kotoba] to iu', english: 'say [word] to [person]' },
      { japanese: '[物]を使う', romaji: '[mono] o tsukau', english: 'use [object]' },
      { japanese: '[人]に[物]をあげる', romaji: '[hito] ni [mono] o ageru', english: 'give [object] to [person]' },
      { japanese: '[物]を開ける', romaji: '[mono] o akeru', english: 'open [object]' },
      { japanese: '[物]を閉める', romaji: '[mono] o shimeru', english: 'close [object]' },
      { japanese: '[食べ物]を食べる', romaji: '[tabemono] o taberu', english: 'eat [food]' },
      { japanese: '[飲み物]を飲む', romaji: '[nomimono] o nomu', english: 'drink [beverage]' },
      { japanese: '持ち物', romaji: 'mochimono', english: 'inventory' },
      { japanese: 'ヘルプ', romaji: 'herupu', english: 'help' }
    ];

    commands.forEach(cmd => {
      this.addToGameLog({
        japanese: `- ${cmd.japanese}`,
        romaji: `- ${cmd.romaji}`,
        english: `- ${cmd.english}`
      });
    });
  }

  // Look at an object
  lookAtObject(objectName) {
    // Check if the object is an item in the room
    const room = this.getCurrentRoom();
    const roomItems = room.items || [];

    // Find the item in the room
    const roomItem = roomItems.find(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.japanese === objectName ||
        item.name.romaji.toLowerCase() === objectName.toLowerCase() ||
        item.name.english.toLowerCase() === objectName.toLowerCase()
      );
    });

    if (roomItem) {
      const item = getItemById(roomItem);
      this.addToGameLog({
        japanese: item.description.japanese,
        romaji: item.description.romaji,
        english: item.description.english
      });

      // Learn vocabulary from this item
      if (item.targetVocabulary) {
        item.targetVocabulary.forEach(word => {
          this.gameState.learnedVocabulary.add(word);
        });
      }
      return;
    }

    // Check if the object is in the inventory
    const inventoryItem = this.gameState.inventory.find(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.japanese === objectName ||
        item.name.romaji.toLowerCase() === objectName.toLowerCase() ||
        item.name.english.toLowerCase() === objectName.toLowerCase()
      );
    });

    if (inventoryItem) {
      const item = getItemById(inventoryItem);
      this.addToGameLog({
        japanese: item.description.japanese,
        romaji: item.description.romaji,
        english: item.description.english
      });

      // Learn vocabulary from this item
      if (item.targetVocabulary) {
        item.targetVocabulary.forEach(word => {
          this.gameState.learnedVocabulary.add(word);
        });
      }
      return;
    }

    // Check if the object is an NPC in the room
    const roomNpcs = room.npcs || [];
    const roomNpc = roomNpcs.find(npcId => {
      const npc = getNpcById(npcId);
      return npc && (
        npc.name.romanian.toLowerCase() === objectName.toLowerCase() ||
        npc.name.english.toLowerCase() === objectName.toLowerCase()
      );
    });

    if (roomNpc) {
      const npc = getNpcById(roomNpc);
      this.addToGameLog({
        romanian: npc.description.romanian,
        english: npc.description.english
      });

      // Learn vocabulary from this NPC
      if (npc.targetVocabulary) {
        npc.targetVocabulary.forEach(word => {
          this.gameState.learnedVocabulary.add(word);
        });
      }
      return;
    }

    // Object not found
    this.addToGameLog({
      romanian: `Nu văd ${objectName} aici.`,
      english: `I don't see ${objectName} here.`
    });
  }

  // Move to a direction
  moveToDirection(direction) {
    const room = this.getCurrentRoom();

    if (!room.exits || !room.exits[direction]) {
      this.addToGameLog({
        romanian: `Nu poți merge în direcția ${direction}.`,
        english: `You can't go ${direction}.`
      });
      return;
    }

    // Special case for the locked door to the secret room
    if (room.id === 'bedroom' && direction === 'east') {
      // Check if the player has the key
      if (!this.gameState.inventory.includes('key')) {
        this.addToGameLog({
          japanese: 'ドアは施錠されています。鍵が必要です。',
          romaji: 'Doa wa sejō sarete imasu. Kagi ga hitsuyoō desu.',
          english: 'The door is locked. You need a key.'
        });
        return;
      }
    }

    // Move to the new room
    const newRoomId = room.exits[direction];
    this.gameState.currentRoomId = newRoomId;

    // Mark the room as visited
    this.gameState.visitedRooms.add(newRoomId);

    // Clear the game log before describing the new room
    this.gameState.gameLog = [];

    // Add a movement message
    const directionMap = {
      'north': '北',
      'south': '南',
      'east': '東',
      'west': '西',
      'up': '上',
      'down': '下'
    };

    const romajiDirectionMap = {
      'north': 'kita',
      'south': 'minami',
      'east': 'higashi',
      'west': 'nishi',
      'up': 'ue',
      'down': 'shita'
    };

    this.addToGameLog({
      japanese: `あなたは${directionMap[direction] || direction}に移動しました。`,
      romaji: `Anata wa ${romajiDirectionMap[direction] || direction} ni idō shimashita.`,
      english: `You moved ${direction}.`
    });

    // Describe the new room
    this.describeCurrentRoom();
  }

  // Take an item
  takeItem(itemName) {
    const room = this.getCurrentRoom();
    const roomItems = room.items || [];

    // Find the item in the room
    const itemIndex = roomItems.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.japanese === itemName ||
        item.name.romaji.toLowerCase() === itemName.toLowerCase() ||
        item.name.english.toLowerCase() === itemName.toLowerCase()
      );
    });

    if (itemIndex === -1) {
      this.addToGameLog({
        japanese: `ここに${itemName}は見えません。`,
        romaji: `Koko ni ${itemName} wa miemasen.`,
        english: `I don't see ${itemName} here.`
      });
      return;
    }

    const itemId = roomItems[itemIndex];
    const item = getItemById(itemId);

    if (!item.canTake) {
      this.addToGameLog({
        japanese: `${item.name.japanese}を取ることができません。`,
        romaji: `${item.name.romaji} o toru koto ga dekimasen.`,
        english: `You can't take ${item.name.english}.`
      });
      return;
    }

    // Remove the item from the room
    room.items.splice(itemIndex, 1);

    // Add the item to the inventory
    this.gameState.inventory.push(itemId);

    this.addToGameLog({
      romanian: `Ai luat ${item.name.romanian}.`,
      english: `You took ${item.name.english}.`
    });

    // Learn vocabulary from this item
    if (item.targetVocabulary) {
      item.targetVocabulary.forEach(word => {
        this.gameState.learnedVocabulary.add(word);
      });
    }
  }

  // Drop an item
  dropItem(itemName) {
    // Find the item in the inventory
    const itemIndex = this.gameState.inventory.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.romanian.toLowerCase() === itemName.toLowerCase() ||
        item.name.english.toLowerCase() === itemName.toLowerCase()
      );
    });

    if (itemIndex === -1) {
      this.addToGameLog({
        romanian: `Nu ai ${itemName} în inventar.`,
        english: `You don't have ${itemName} in your inventory.`
      });
      return;
    }

    const itemId = this.gameState.inventory[itemIndex];
    const item = getItemById(itemId);

    // Remove the item from the inventory
    this.gameState.inventory.splice(itemIndex, 1);

    // Add the item to the room
    const room = this.getCurrentRoom();
    if (!room.items) {
      room.items = [];
    }
    room.items.push(itemId);

    this.addToGameLog({
      romanian: `Ai lăsat ${item.name.romanian}.`,
      english: `You dropped ${item.name.english}.`
    });
  }

  // Show inventory
  showInventory() {
    if (this.gameState.inventory.length === 0) {
      this.addToGameLog({
        romanian: 'Inventarul tău este gol.',
        english: 'Your inventory is empty.'
      });
      return;
    }

    const itemNames = this.gameState.inventory.map(itemId => {
      const item = getItemById(itemId);
      return item ? item.name.romanian : '';
    }).filter(Boolean);

    this.addToGameLog({
      romanian: `Inventar: ${itemNames.join(', ')}`,
      english: `Inventory: ${itemNames.join(', ')}`
    });
  }

  // Use an item
  useItem(itemName, targetName = null) {
    // Find the item in the inventory
    const itemIndex = this.gameState.inventory.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.romanian.toLowerCase() === itemName.toLowerCase() ||
        item.name.english.toLowerCase() === itemName.toLowerCase()
      );
    });

    if (itemIndex === -1) {
      this.addToGameLog({
        romanian: `Nu ai ${itemName} în inventar.`,
        english: `You don't have ${itemName} in your inventory.`
      });
      return;
    }

    const itemId = this.gameState.inventory[itemIndex];
    const item = getItemById(itemId);

    if (!item.canUse) {
      this.addToGameLog({
        romanian: `Nu poți folosi ${item.name.romanian}.`,
        english: `You can't use ${item.name.english}.`
      });
      return;
    }

    // Special case for using the key on the bedroom door
    if (itemId === 'key' && this.gameState.currentRoomId === 'bedroom') {
      this.addToGameLog({
        romanian: 'Ai folosit cheia pentru a deschide ușa.',
        english: 'You used the key to unlock the door.'
      });
      return;
    }

    // Special case for using the book
    if (itemId === 'book' || itemId === 'old_book') {
      this.addToGameLog({
        romanian: 'Ai citit cartea și ai învățat cuvinte noi în română.',
        english: 'You read the book and learned new Romanian words.'
      });
      return;
    }

    // Generic use message
    this.addToGameLog({
      romanian: `Ai folosit ${item.name.romanian}.`,
      english: `You used ${item.name.english}.`
    });
  }

  // Open an object
  openObject(objectName) {
    // Check if the object is in the inventory
    const inventoryItemIndex = this.gameState.inventory.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.romanian.toLowerCase() === objectName.toLowerCase() ||
        item.name.english.toLowerCase() === objectName.toLowerCase()
      );
    });

    if (inventoryItemIndex !== -1) {
      const itemId = this.gameState.inventory[inventoryItemIndex];
      const item = getItemById(itemId);

      if (!item.canOpen) {
        this.addToGameLog({
          romanian: `Nu poți deschide ${item.name.romanian}.`,
          english: `You can't open ${item.name.english}.`
        });
        return;
      }

      // Special case for opening the old book
      if (itemId === 'old_book') {
        this.addToGameLog({
          romanian: 'Ai deschis cartea veche și ai găsit o notă înăuntru.',
          english: 'You opened the old book and found a note inside.'
        });

        // Add the note to the inventory if it's not already there
        if (!this.gameState.inventory.includes('note')) {
          this.gameState.inventory.push('note');
        }
        return;
      }

      this.addToGameLog({
        romanian: `Ai deschis ${item.name.romanian}.`,
        english: `You opened ${item.name.english}.`
      });
      return;
    }

    // Check if the object is in the room
    const room = this.getCurrentRoom();
    const roomItemIndex = room.items ? room.items.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.romanian.toLowerCase() === objectName.toLowerCase() ||
        item.name.english.toLowerCase() === objectName.toLowerCase()
      );
    }) : -1;

    if (roomItemIndex !== -1) {
      const itemId = room.items[roomItemIndex];
      const item = getItemById(itemId);

      if (!item.canOpen) {
        this.addToGameLog({
          romanian: `Nu poți deschide ${item.name.romanian}.`,
          english: `You can't open ${item.name.english}.`
        });
        return;
      }

      this.addToGameLog({
        romanian: `Ai deschis ${item.name.romanian}.`,
        english: `You opened ${item.name.english}.`
      });
      return;
    }

    // Object not found
    this.addToGameLog({
      romanian: `Nu văd ${objectName} aici.`,
      english: `I don't see ${objectName} here.`
    });
  }

  // Close an object
  closeObject(objectName) {
    // Similar to openObject but for closing
    this.addToGameLog({
      romanian: `Ai închis ${objectName}.`,
      english: `You closed ${objectName}.`
    });
  }

  // Eat an item
  eatItem(itemName) {
    // Find the item in the inventory
    const itemIndex = this.gameState.inventory.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.romanian.toLowerCase() === itemName.toLowerCase() ||
        item.name.english.toLowerCase() === itemName.toLowerCase()
      );
    });

    if (itemIndex === -1) {
      this.addToGameLog({
        romanian: `Nu ai ${itemName} în inventar.`,
        english: `You don't have ${itemName} in your inventory.`
      });
      return;
    }

    const itemId = this.gameState.inventory[itemIndex];

    // Special case for bread
    if (itemId === 'bread') {
      // Remove the bread from the inventory
      this.gameState.inventory.splice(itemIndex, 1);

      this.addToGameLog({
        romanian: 'Ai mâncat pâinea. Era delicioasă!',
        english: 'You ate the bread. It was delicious!'
      });
      return;
    }

    // Can't eat other items
    this.addToGameLog({
      romanian: `Nu poți mânca ${itemName}.`,
      english: `You can't eat ${itemName}.`
    });
  }

  // Drink an item
  drinkItem(itemName) {
    // Find the item in the inventory
    const itemIndex = this.gameState.inventory.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.romanian.toLowerCase() === itemName.toLowerCase() ||
        item.name.english.toLowerCase() === itemName.toLowerCase()
      );
    });

    if (itemIndex === -1) {
      this.addToGameLog({
        romanian: `Nu ai ${itemName} în inventar.`,
        english: `You don't have ${itemName} in your inventory.`
      });
      return;
    }

    const itemId = this.gameState.inventory[itemIndex];

    // Special case for water
    if (itemId === 'water') {
      // Remove the water from the inventory
      this.gameState.inventory.splice(itemIndex, 1);

      this.addToGameLog({
        romanian: 'Ai băut apa. Era răcoritoare!',
        english: 'You drank the water. It was refreshing!'
      });
      return;
    }

    // Can't drink other items
    this.addToGameLog({
      romanian: `Nu poți bea ${itemName}.`,
      english: `You can't drink ${itemName}.`
    });
  }

  // Talk to an NPC
  talkToNpc(npcName) {
    const room = this.getCurrentRoom();
    const roomNpcs = room.npcs || [];

    // Find the NPC in the room
    const npcIndex = roomNpcs.findIndex(npcId => {
      const npc = getNpcById(npcId);
      return npc && (
        npc.name.japanese === npcName ||
        npc.name.romaji.toLowerCase() === npcName.toLowerCase() ||
        npc.name.english.toLowerCase() === npcName.toLowerCase()
      );
    });

    if (npcIndex === -1) {
      this.addToGameLog({
        japanese: `ここに${npcName}はいません。`,
        romaji: `Koko ni ${npcName} wa imasen.`,
        english: `I don't see ${npcName} here.`
      });
      return;
    }

    const npcId = roomNpcs[npcIndex];
    const npc = getNpcById(npcId);

    // Display the NPC's greeting
    this.addToGameLog({
      japanese: `${npc.name.japanese}: 「${npc.dialogue.greeting.japanese}」`,
      romaji: `${npc.name.romaji}: "${npc.dialogue.greeting.romaji}"`,
      english: `${npc.name.english}: "${npc.dialogue.greeting.english}"`
    });

    // Learn vocabulary from this NPC
    if (npc.targetVocabulary) {
      npc.targetVocabulary.forEach(word => {
        this.gameState.learnedVocabulary.add(word);
      });
    }
  }

  // Say something to an NPC
  sayToNpc(phrase, npcName) {
    const room = this.getCurrentRoom();
    const roomNpcs = room.npcs || [];

    // Find the NPC in the room
    const npcIndex = roomNpcs.findIndex(npcId => {
      const npc = getNpcById(npcId);
      return npc && (
        npc.name.japanese === npcName ||
        npc.name.romaji.toLowerCase() === npcName.toLowerCase() ||
        npc.name.english.toLowerCase() === npcName.toLowerCase()
      );
    });

    if (npcIndex === -1) {
      this.addToGameLog({
        japanese: `ここに${npcName}はいません。`,
        romaji: `Koko ni ${npcName} wa imasen.`,
        english: `I don't see ${npcName} here.`
      });
      return;
    }

    const npcId = roomNpcs[npcIndex];
    const npc = getNpcById(npcId);

    // Get the NPC's response based on the phrase
    const response = getNpcResponse(npcId, phrase);

    if (response) {
      this.addToGameLog({
        japanese: `${npc.name.japanese}: 「${response.japanese}」`,
        romaji: `${npc.name.romaji}: "${response.romaji}"`,
        english: `${npc.name.english}: "${response.english}"`
      });
    } else {
      this.addToGameLog({
        japanese: `${npc.name.japanese}はあなたの言っていることが理解できません。`,
        romaji: `${npc.name.romaji} wa anata no itte iru koto ga rikai dekimasen.`,
        english: `${npc.name.english} doesn't understand what you're saying.`
      });
    }
  }

  // Give an item to an NPC
  giveItemToNpc(itemName, npcName) {
    // Find the item in the inventory
    const itemIndex = this.gameState.inventory.findIndex(itemId => {
      const item = getItemById(itemId);
      return item && (
        item.name.japanese === itemName ||
        item.name.romaji.toLowerCase() === itemName.toLowerCase() ||
        item.name.english.toLowerCase() === itemName.toLowerCase()
      );
    });

    if (itemIndex === -1) {
      this.addToGameLog({
        japanese: `あなたの持ち物に${itemName}はありません。`,
        romaji: `Anata no mochimono ni ${itemName} wa arimasen.`,
        english: `You don't have ${itemName} in your inventory.`
      });
      return;
    }

    // Find the NPC in the room
    const room = this.getCurrentRoom();
    const roomNpcs = room.npcs || [];

    const npcIndex = roomNpcs.findIndex(npcId => {
      const npc = getNpcById(npcId);
      return npc && (
        npc.name.japanese === npcName ||
        npc.name.romaji.toLowerCase() === npcName.toLowerCase() ||
        npc.name.english.toLowerCase() === npcName.toLowerCase()
      );
    });

    if (npcIndex === -1) {
      this.addToGameLog({
        japanese: `ここに${npcName}はいません。`,
        romaji: `Koko ni ${npcName} wa imasen.`,
        english: `I don't see ${npcName} here.`
      });
      return;
    }

    const itemId = this.gameState.inventory[itemIndex];
    const item = getItemById(itemId);

    const npcId = roomNpcs[npcIndex];
    const npc = getNpcById(npcId);

    // Remove the item from the inventory
    this.gameState.inventory.splice(itemIndex, 1);

    // Add the item to the NPC's inventory
    if (!npc.inventory) {
      npc.inventory = [];
    }
    npc.inventory.push(itemId);

    this.addToGameLog({
      japanese: `あなたは${npc.name.japanese}に${item.name.japanese}をあげました。`,
      romaji: `Anata wa ${npc.name.romaji} ni ${item.name.romaji} o agemashita.`,
      english: `You gave ${item.name.english} to ${npc.name.english}.`
    });
  }

  // Show inventory
  showInventory() {
    if (this.gameState.inventory.length === 0) {
      this.addToGameLog({
        japanese: 'あなたは何も持っていません。',
        romaji: 'Anata wa nanimo motte imasen.',
        english: 'You are not carrying anything.'
      });
      return;
    }

    this.addToGameLog({
      japanese: 'あなたは次のものを持っています：',
      romaji: 'Anata wa tsugi no mono o motte imasu:',
      english: 'You are carrying:'
    });

    this.gameState.inventory.forEach(itemId => {
      const item = getItemById(itemId);
      if (item) {
        this.addToGameLog({
          japanese: `- ${item.name.japanese}`,
          romaji: `- ${item.name.romaji}`,
          english: `- ${item.name.english}`
        });
      }
    });
  }

  // Get the game state
  getGameState() {
    return this.gameState;
  }
}

// Create and export a singleton instance
const gameEngine = new GameEngine();
export default gameEngine;
