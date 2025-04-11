import { useState, useEffect, useRef } from 'react';
import CommandInput from './CommandInput';
import GameOutput from './GameOutput';
import GameVisuals from './GameVisuals';
import SoundManager from './SoundManager';
import gameEngine from '../engine/GameEngine';
import { preloadAssets, playSound } from '../utils/assetManager';

const GameConsole = () => {
  const [gameState, setGameState] = useState(null);
  const [previousGameState, setPreviousGameState] = useState(null);
  const [showVisuals, setShowVisuals] = useState(true);
  const outputRef = useRef(null);

  // Preload assets when the component mounts
  useEffect(() => {
    preloadAssets();
  }, []);

  // Initialize the game when the component mounts
  useEffect(() => {
    const initialState = gameEngine.initGame();
    setGameState(initialState);
    setPreviousGameState(initialState);

    // Play startup sound
    playSound('ui_confirm');
  }, []);

  // Scroll to the bottom of the output when new messages are added
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [gameState?.gameLog]);

  // Handle command submission
  const handleCommand = (command) => {
    if (!command.trim()) return;

    // Play UI sound
    playSound('ui_select');

    // Save the current state before updating
    setPreviousGameState({ ...gameState });

    // Process the command and update the game state
    const newState = gameEngine.processCommand(command);
    setGameState({ ...newState });
  };

  // Toggle visuals display
  const toggleVisuals = () => {
    playSound('ui_select');
    setShowVisuals(!showVisuals);
  };

  // If the game state is not initialized yet, show a loading message
  if (!gameState) {
    return <div className="game-console">Loading...</div>;
  }

  return (
    <div className="game-console">
      {/* Sound Manager */}
      <SoundManager gameState={gameState} previousGameState={previousGameState} />

      <div className="game-header">
        <h1>Japanese Adventure</h1>
        <div className="game-stats">
          <div>
            <strong>Room:</strong> {gameState.currentRoomId}
          </div>
          <div>
            <strong>Vocabulary Learned:</strong> {gameState.learnedVocabulary.size}
          </div>
          <div>
            <button onClick={toggleVisuals} className="toggle-visuals-btn">
              {showVisuals ? 'Hide Visuals' : 'Show Visuals'}
            </button>
          </div>
        </div>
      </div>

      <div className="game-content">
        {showVisuals && (
          <div className="game-visuals-container">
            <GameVisuals gameState={gameState} previousGameState={previousGameState} />
          </div>
        )}

        <div className={`game-output-container ${showVisuals ? 'with-visuals' : 'full-width'}`} ref={outputRef}>
          <GameOutput gameLog={gameState.gameLog} />
        </div>
      </div>

      <CommandInput onSubmit={handleCommand} />

      <div className="game-footer">
        <p>Type "help" for available commands</p>
      </div>
    </div>
  );
};

export default GameConsole;
