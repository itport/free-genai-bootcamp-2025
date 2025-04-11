/**
 * Asset Manager for Romanian Adventure Game
 * Manages loading and accessing game assets (images, sounds, etc.)
 */

// Room images - using retro pixel art style
const roomImages = {
  // Starting Room
  start: '/images/rooms/starting_room.svg',
  // Living Room
  living_room: '/images/rooms/living_room.svg',
  // Kitchen
  kitchen: '/images/rooms/kitchen.svg',
  // Bedroom
  bedroom: '/images/rooms/bedroom.svg',
  // Secret Room
  locked_room: '/images/rooms/secret_room.svg',
  // Default Room
  default: '/images/rooms/default.svg'
};

// Item images
const itemImages = {
  key: '/images/items/key.svg',
  book: '/images/items/book.svg',
  old_book: '/images/items/old_book.svg',
  chair: '/images/items/chair.svg',
  bread: '/images/items/bread.svg',
  water: '/images/items/water.svg',
  note: '/images/items/note.svg',
  default: '/images/items/default.svg'
};

// NPC images
const npcImages = {
  old_man: '/images/npcs/old_man.svg',
  default: '/images/npcs/default.svg'
};

// Sound effects
const soundEffects = {
  // UI sounds
  ui_select: '/assets/sounds/ui_select.wav',
  ui_confirm: '/assets/sounds/ui_confirm.wav',
  ui_cancel: '/assets/sounds/ui_cancel.wav',

  // Action sounds
  door_open: '/assets/sounds/door_open.wav',
  door_close: '/assets/sounds/door_close.wav',
  door_locked: '/assets/sounds/door_locked.wav',
  item_pickup: '/assets/sounds/item_pickup.wav',
  item_drop: '/assets/sounds/item_drop.wav',
  book_open: '/assets/sounds/book_open.wav',
  key_use: '/assets/sounds/key_use.wav',
  eat: '/assets/sounds/eat.wav',
  drink: '/assets/sounds/drink.wav',

  // Ambient sounds
  ambient_room: '/assets/sounds/ambient_room.wav',
  ambient_kitchen: '/assets/sounds/ambient_kitchen.wav',
  ambient_secret: '/assets/sounds/ambient_secret.wav'
};

// Animation frames for items and NPCs
const animations = {
  key: {
    idle: [
      '/images/items/key.svg',
      '/images/items/key.svg'
    ]
  },
  old_book: {
    idle: [
      '/images/items/old_book.svg',
      '/images/items/old_book.svg'
    ]
  },
  old_man: {
    idle: [
      '/images/npcs/old_man.svg',
      '/images/npcs/old_man.svg'
    ],
    talking: [
      '/images/npcs/old_man.svg',
      '/images/npcs/old_man.svg',
      '/images/npcs/old_man.svg'
    ]
  }
};

// Preload assets
const preloadAssets = () => {
  // Preload images
  const allImages = [
    ...Object.values(roomImages),
    ...Object.values(itemImages),
    ...Object.values(npcImages)
  ];

  // Preload animation frames
  Object.values(animations).forEach(animationSet => {
    Object.values(animationSet).forEach(frames => {
      allImages.push(...frames);
    });
  });

  // Create Image objects for preloading
  allImages.forEach(src => {
    const img = new Image();
    img.src = src;
  });

  // Preload sounds
  Object.values(soundEffects).forEach(src => {
    const audio = new Audio();
    audio.src = src;
  });
};

// Play a sound effect
const playSound = (soundName) => {
  const soundSrc = soundEffects[soundName];
  if (!soundSrc) return;

  const audio = new Audio(soundSrc);
  audio.play().catch(error => {
    console.warn(`Failed to play sound: ${soundName}`, error);
  });
};

// Get room image by room ID
const getRoomImage = (roomId) => {
  return roomImages[roomId] || roomImages.default;
};

// Get item image by item ID
const getItemImage = (itemId) => {
  return itemImages[itemId] || itemImages.default;
};

// Get NPC image by NPC ID
const getNpcImage = (npcId) => {
  return npcImages[npcId] || npcImages.default;
};

// Get animation frames for an entity
const getAnimationFrames = (entityType, entityId, animationName = 'idle') => {
  if (!animations[entityId] || !animations[entityId][animationName]) {
    return null;
  }

  return animations[entityId][animationName];
};

export {
  preloadAssets,
  playSound,
  getRoomImage,
  getItemImage,
  getNpcImage,
  getAnimationFrames
};
