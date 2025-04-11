import { useState, useEffect, useRef } from 'react';
import AnimatedSprite from './AnimatedSprite';
import RoomTransition from './RoomTransition';

const RetroGameVisuals = ({ gameState, previousGameState }) => {
  const [roomImage, setRoomImage] = useState('');
  const [roomNpcs, setRoomNpcs] = useState([]);
  const [roomItems, setRoomItems] = useState([]);
  const [animatingNpc, setAnimatingNpc] = useState(null);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [transitionDirection, setTransitionDirection] = useState(null);
  const [hoveredItem, setHoveredItem] = useState(null);
  const [hoveredNpc, setHoveredNpc] = useState(null);
  const previousRoomRef = useRef(null);

  // Update room image when the current room changes
  useEffect(() => {
    if (gameState && gameState.currentRoomId) {
      // Check if room has changed
      if (previousRoomRef.current && previousRoomRef.current !== gameState.currentRoomId) {
        // Determine transition direction based on room change
        const direction = determineTransitionDirection(previousRoomRef.current, gameState.currentRoomId);
        setTransitionDirection(direction);
        setIsTransitioning(true);
      }

      // Set the room image based on the current room
      let roomId = gameState.currentRoomId;
      // Use the correct path for the room image
      const roomImagePath = `/images/rooms/${roomId}.svg`;
      console.log('Room image path:', roomImagePath);
      setRoomImage(roomImagePath);

      // Get NPCs in the current room
      const currentRoom = gameState.currentRoomId;
      import('../data/rooms').then(({ getRoomById }) => {
        const room = getRoomById(currentRoom);
        if (room && room.npcs) {
          setRoomNpcs(room.npcs);
        } else {
          setRoomNpcs([]);
        }

        if (room && room.items) {
          setRoomItems(room.items);
        } else {
          setRoomItems([]);
        }
      });

      // Update previous room reference
      previousRoomRef.current = gameState.currentRoomId;
    }
  }, [gameState?.currentRoomId]);

  // Check for NPC interactions in the game log
  useEffect(() => {
    if (!gameState?.gameLog || gameState.gameLog.length === 0) return;

    const latestLog = gameState.gameLog[gameState.gameLog.length - 1];
    const message = latestLog.message.english.toLowerCase();

    // Check if the message involves talking to an NPC
    if (message.includes('old man') && (message.includes('talk') || message.includes('say'))) {
      // Set the NPC to animate
      setAnimatingNpc('old_man');

      // Stop the animation after 3 seconds
      const timer = setTimeout(() => {
        setAnimatingNpc(null);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [gameState?.gameLog]);

  // Determine transition direction based on room change
  const determineTransitionDirection = (fromRoom, toRoom) => {
    // This is a simplified example - in a real game, you would have a map of room connections
    // For now, we'll just return a random direction
    const directions = ['north', 'south', 'east', 'west'];
    return directions[Math.floor(Math.random() * directions.length)];
  };

  // Handle transition completion
  const handleTransitionComplete = () => {
    setIsTransitioning(false);
  };

  // Handle item hover
  const handleItemHover = (itemId) => {
    setHoveredItem(itemId);
  };

  // Handle NPC hover
  const handleNpcHover = (npcId) => {
    setHoveredNpc(npcId);
  };

  return (
    <div className="retro-game-visuals">
      {/* Room Transition Effect */}
      {isTransitioning && (
        <RoomTransition
          isTransitioning={isTransitioning}
          fromRoomId={previousRoomRef.current}
          toRoomId={gameState.currentRoomId}
          direction={transitionDirection}
          onTransitionComplete={handleTransitionComplete}
        />
      )}

      <div className="room-display">
        <h3>Location: {gameState.currentRoomId.replace('_', ' ')}</h3>
        <div className="room-image-container">
          <img
            src={roomImage}
            alt={`Room: ${gameState.currentRoomId}`}
            className="room-image"
          />

          {/* Display NPCs in the room */}
          {roomNpcs.map(npcId => (
            <div
              key={npcId}
              className="room-npc"
              onMouseEnter={() => handleNpcHover(npcId)}
              onMouseLeave={() => setHoveredNpc(null)}
            >
              <AnimatedSprite
                entityType="npc"
                entityId={npcId}
                animationName={animatingNpc === npcId ? 'talking' : 'idle'}
                fps={6}
                isPlaying={true}
                scale={hoveredNpc === npcId ? 1.1 : 1}
              />
            </div>
          ))}

          {/* Display items in the room that are not in inventory */}
          {roomItems.filter(itemId => !gameState.inventory.includes(itemId)).map(itemId => (
            <div
              key={itemId}
              className="room-item"
              onMouseEnter={() => handleItemHover(itemId)}
              onMouseLeave={() => setHoveredItem(null)}
            >
              <AnimatedSprite
                entityType="item"
                entityId={itemId}
                fps={3}
                isPlaying={true}
                scale={hoveredItem === itemId ? 1.2 : 1}
                rotation={hoveredItem === itemId ? 5 : 0}
              />
            </div>
          ))}
        </div>
      </div>

      {gameState?.inventory && gameState.inventory.length > 0 && (
        <div className="inventory-display">
          <h3>Inventory</h3>
          <div className="inventory-grid">
            {gameState.inventory.map(itemId => (
              <div
                key={itemId}
                className="inventory-item-card"
                onMouseEnter={() => handleItemHover(itemId)}
                onMouseLeave={() => setHoveredItem(null)}
              >
                <AnimatedSprite
                  entityType="item"
                  entityId={itemId}
                  fps={2}
                  isPlaying={true}
                  scale={hoveredItem === itemId ? 1.2 : 1}
                  rotation={hoveredItem === itemId ? 5 : 0}
                />
                <span className="item-name">{itemId.replace('_', ' ')}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {gameState?.learnedVocabulary && gameState.learnedVocabulary.size > 0 && (
        <div className="vocabulary-display">
          <h3>Vocabulary Learned: {gameState.learnedVocabulary.size}</h3>
          <div className="vocabulary-grid">
            {Array.from(gameState.learnedVocabulary).map(word => (
              <div key={word} className="vocabulary-card">
                {word}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RetroGameVisuals;
