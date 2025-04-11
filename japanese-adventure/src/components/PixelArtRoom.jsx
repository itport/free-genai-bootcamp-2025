import { useEffect, useRef } from 'react';

const PixelArtRoom = ({ roomId }) => {
  const canvasRef = useRef(null);
  
  // Draw the pixel art for the room
  useEffect(() => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Set the pixel size
    const pixelSize = 10;
    
    // Draw the room based on the roomId
    switch (roomId) {
      case 'start':
        drawStartingRoom(ctx, pixelSize);
        break;
      case 'living_room':
        drawLivingRoom(ctx, pixelSize);
        break;
      case 'kitchen':
        drawKitchen(ctx, pixelSize);
        break;
      case 'bedroom':
        drawBedroom(ctx, pixelSize);
        break;
      case 'locked_room':
        drawSecretRoom(ctx, pixelSize);
        break;
      default:
        drawDefaultRoom(ctx, pixelSize);
    }
  }, [roomId]);
  
  return (
    <div className="pixel-art-container">
      <canvas 
        ref={canvasRef} 
        width={300} 
        height={200} 
        className="pixel-art-canvas"
      />
    </div>
  );
};

// Helper functions to draw each room
const drawStartingRoom = (ctx, pixelSize) => {
  // Floor
  drawRect(ctx, 0, 0, 30, 20, '#333', pixelSize);
  
  // Walls
  drawRect(ctx, 0, 0, 30, 2, '#555', pixelSize);
  drawRect(ctx, 0, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 28, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 0, 18, 30, 2, '#555', pixelSize);
  
  // Table
  drawRect(ctx, 12, 8, 6, 4, '#8B4513', pixelSize);
  
  // Door
  drawRect(ctx, 14, 18, 4, 2, '#8B4513', pixelSize);
  
  // Key on table
  drawRect(ctx, 14, 7, 2, 1, '#FFD700', pixelSize);
  
  // Book on table
  drawRect(ctx, 16, 8, 1, 2, '#00008B', pixelSize);
};

const drawLivingRoom = (ctx, pixelSize) => {
  // Floor
  drawRect(ctx, 0, 0, 30, 20, '#3a3a3a', pixelSize);
  
  // Walls
  drawRect(ctx, 0, 0, 30, 2, '#555', pixelSize);
  drawRect(ctx, 0, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 28, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 0, 18, 30, 2, '#555', pixelSize);
  
  // Chair
  drawRect(ctx, 5, 10, 4, 4, '#8B4513', pixelSize);
  
  // Window
  drawRect(ctx, 20, 2, 6, 4, '#87CEEB', pixelSize);
  
  // Door to south
  drawRect(ctx, 14, 18, 4, 2, '#8B4513', pixelSize);
  
  // Door to east
  drawRect(ctx, 28, 10, 2, 4, '#8B4513', pixelSize);
  
  // Old man
  drawRect(ctx, 6, 8, 2, 2, '#FFE4B5', pixelSize);
};

const drawKitchen = (ctx, pixelSize) => {
  // Floor
  drawRect(ctx, 0, 0, 30, 20, '#444', pixelSize);
  
  // Walls
  drawRect(ctx, 0, 0, 30, 2, '#555', pixelSize);
  drawRect(ctx, 0, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 28, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 0, 18, 30, 2, '#555', pixelSize);
  
  // Small table
  drawRect(ctx, 12, 10, 4, 3, '#8B4513', pixelSize);
  
  // Refrigerator
  drawRect(ctx, 22, 3, 4, 6, '#DCDCDC', pixelSize);
  
  // Bread on table
  drawRect(ctx, 13, 9, 2, 1, '#F5DEB3', pixelSize);
  
  // Water on table
  drawRect(ctx, 15, 9, 1, 1, '#00BFFF', pixelSize);
  
  // Door to west
  drawRect(ctx, 0, 10, 2, 4, '#8B4513', pixelSize);
  
  // Door to north
  drawRect(ctx, 14, 0, 4, 2, '#8B4513', pixelSize);
};

const drawBedroom = (ctx, pixelSize) => {
  // Floor
  drawRect(ctx, 0, 0, 30, 20, '#4a4a4a', pixelSize);
  
  // Walls
  drawRect(ctx, 0, 0, 30, 2, '#555', pixelSize);
  drawRect(ctx, 0, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 28, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 0, 18, 30, 2, '#555', pixelSize);
  
  // Bed
  drawRect(ctx, 5, 5, 10, 6, '#8B4513', pixelSize);
  drawRect(ctx, 5, 5, 10, 1, '#4169E1', pixelSize);
  
  // Door to south
  drawRect(ctx, 14, 18, 4, 2, '#8B4513', pixelSize);
  
  // Locked door to east
  drawRect(ctx, 28, 10, 2, 4, '#8B0000', pixelSize);
};

const drawSecretRoom = (ctx, pixelSize) => {
  // Floor
  drawRect(ctx, 0, 0, 30, 20, '#2a2a2a', pixelSize);
  
  // Walls
  drawRect(ctx, 0, 0, 30, 2, '#555', pixelSize);
  drawRect(ctx, 0, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 28, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 0, 18, 30, 2, '#555', pixelSize);
  
  // Table with old book
  drawRect(ctx, 12, 8, 6, 4, '#8B4513', pixelSize);
  drawRect(ctx, 14, 7, 2, 2, '#8B0000', pixelSize);
  
  // Door to west
  drawRect(ctx, 0, 10, 2, 4, '#8B4513', pixelSize);
  
  // Mysterious glow
  drawRect(ctx, 14, 6, 2, 1, '#FFFF00', pixelSize);
};

const drawDefaultRoom = (ctx, pixelSize) => {
  // Floor
  drawRect(ctx, 0, 0, 30, 20, '#333', pixelSize);
  
  // Walls
  drawRect(ctx, 0, 0, 30, 2, '#555', pixelSize);
  drawRect(ctx, 0, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 28, 0, 2, 20, '#555', pixelSize);
  drawRect(ctx, 0, 18, 30, 2, '#555', pixelSize);
};

// Helper function to draw a rectangle of pixels
const drawRect = (ctx, x, y, width, height, color, pixelSize) => {
  ctx.fillStyle = color;
  for (let i = 0; i < width; i++) {
    for (let j = 0; j < height; j++) {
      ctx.fillRect(
        (x + i) * pixelSize, 
        (y + j) * pixelSize, 
        pixelSize - 1, 
        pixelSize - 1
      );
    }
  }
};

export default PixelArtRoom;
