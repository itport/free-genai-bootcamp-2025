import { useState, useEffect } from 'react';
import asciiArt from '../data/asciiArt';
import PixelArtRoom from './PixelArtRoom';
import RetroGameVisuals from './RetroGameVisuals';

const GameVisuals = ({ gameState, previousGameState }) => {
  const [currentVisual, setCurrentVisual] = useState(null);
  const [visualMode, setVisualMode] = useState('retro'); // 'retro', 'pixel', or 'ascii'

  useEffect(() => {
    if (gameState && gameState.currentRoomId) {
      // Get the ASCII art for the current room
      const roomArt = asciiArt.rooms[gameState.currentRoomId] || asciiArt.rooms.default;
      setCurrentVisual(roomArt);
    }
  }, [gameState?.currentRoomId]);

  const changeVisualMode = (mode) => {
    setVisualMode(mode);
  };

  if (!currentVisual && visualMode === 'ascii') {
    return <div className="game-visuals-loading">Loading visuals...</div>;
  }

  return (
    <div className="game-visuals">
      <div className="visual-toggle">
        <button
          onClick={() => changeVisualMode('retro')}
          className={visualMode === 'retro' ? 'active' : ''}
        >
          Retro Graphics
        </button>
        <button
          onClick={() => changeVisualMode('pixel')}
          className={visualMode === 'pixel' ? 'active' : ''}
        >
          Pixel Art
        </button>
        <button
          onClick={() => changeVisualMode('ascii')}
          className={visualMode === 'ascii' ? 'active' : ''}
        >
          ASCII Art
        </button>
      </div>

      <div className="visual-container">
        {visualMode === 'retro' && (
          <RetroGameVisuals gameState={gameState} previousGameState={previousGameState} />
        )}
        {visualMode === 'pixel' && (
          <PixelArtRoom roomId={gameState.currentRoomId} />
        )}
        {visualMode === 'ascii' && (
          <pre className="ascii-art">{currentVisual}</pre>
        )}
      </div>

      {visualMode !== 'retro' && gameState?.inventory && gameState.inventory.length > 0 && (
        <div className="inventory-visuals">
          <h3>Inventory</h3>
          <div className="inventory-icons">
            {gameState.inventory.map(itemId => {
              const itemArt = asciiArt.items[itemId] || asciiArt.items.default;
              return (
                <div key={itemId} className="inventory-item">
                  <pre className="item-ascii">{itemArt}</pre>
                  <span className="item-name">{itemId}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {visualMode !== 'retro' && gameState?.learnedVocabulary && gameState.learnedVocabulary.size > 0 && (
        <div className="vocabulary-tracker">
          <h3>Vocabulary Learned: {gameState.learnedVocabulary.size}</h3>
          <div className="vocabulary-list">
            {Array.from(gameState.learnedVocabulary).map(word => (
              <span key={word} className="vocabulary-word">{word}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default GameVisuals;
