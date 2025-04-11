import { useEffect, useRef } from 'react';
import { playSound } from '../utils/assetManager';

const SoundManager = ({ gameState, previousGameState }) => {
  const prevRoomRef = useRef(null);
  const prevInventoryRef = useRef([]);
  
  useEffect(() => {
    // Play sound when the component mounts
    playSound('ui_confirm');
    
    // Preload all sounds
    import('../utils/assetManager').then(({ preloadAssets }) => {
      preloadAssets();
    });
  }, []);
  
  useEffect(() => {
    if (!gameState || !previousGameState) return;
    
    // Room change sounds
    if (gameState.currentRoomId !== prevRoomRef.current) {
      // Play door open sound when moving to a new room
      if (prevRoomRef.current) {
        playSound('door_open');
      }
      
      // Play ambient sound based on the room
      if (gameState.currentRoomId === 'kitchen') {
        playSound('ambient_kitchen');
      } else if (gameState.currentRoomId === 'locked_room') {
        playSound('ambient_secret');
      } else {
        playSound('ambient_room');
      }
      
      prevRoomRef.current = gameState.currentRoomId;
    }
    
    // Inventory change sounds
    if (gameState.inventory.length > prevInventoryRef.current.length) {
      // Item picked up
      playSound('item_pickup');
    } else if (gameState.inventory.length < prevInventoryRef.current.length) {
      // Item dropped
      playSound('item_drop');
    }
    
    // Update previous inventory
    prevInventoryRef.current = [...gameState.inventory];
    
    // Check for specific actions in the game log
    const latestLogEntry = gameState.gameLog[gameState.gameLog.length - 1];
    if (latestLogEntry && previousGameState.gameLog.length < gameState.gameLog.length) {
      const message = latestLogEntry.message.english.toLowerCase();
      
      // Door sounds
      if (message.includes('door') && message.includes('open')) {
        playSound('door_open');
      } else if (message.includes('door') && message.includes('close')) {
        playSound('door_close');
      } else if (message.includes('door') && message.includes('locked')) {
        playSound('door_locked');
      }
      
      // Item interaction sounds
      if (message.includes('book') && message.includes('open')) {
        playSound('book_open');
      } else if (message.includes('key') && message.includes('use')) {
        playSound('key_use');
      } else if (message.includes('eat')) {
        playSound('eat');
      } else if (message.includes('drink')) {
        playSound('drink');
      }
    }
  }, [gameState, previousGameState]);
  
  // This component doesn't render anything
  return null;
};

export default SoundManager;
