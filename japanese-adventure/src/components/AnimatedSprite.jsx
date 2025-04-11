import { useState, useEffect, useRef } from 'react';

const AnimatedSprite = ({
  entityType,
  entityId,
  animationName = 'idle',
  fps = 5,
  isPlaying = true,
  scale = 1,
  flipX = false,
  flipY = false,
  rotation = 0,
  onAnimationComplete = null,
  loop = true
}) => {
  const [currentFrame, setCurrentFrame] = useState(0);
  const [frames, setFrames] = useState([]);
  const [isAnimationComplete, setIsAnimationComplete] = useState(false);
  const animationRef = useRef(null);
  const frameCountRef = useRef(0);

  // Load animation frames
  useEffect(() => {
    // Use static SVG images directly
    if (entityType === 'item') {
      const itemImagePath = `/images/items/${entityId}.svg`;
      setFrames([itemImagePath, itemImagePath]); // Use the same image twice for a simple animation
      setCurrentFrame(0);
      setIsAnimationComplete(false);
      frameCountRef.current = 0;
    } else if (entityType === 'npc') {
      const npcImagePath = `/images/npcs/${entityId}.svg`;
      setFrames([npcImagePath, npcImagePath]); // Use the same image twice for a simple animation
      setCurrentFrame(0);
      setIsAnimationComplete(false);
      frameCountRef.current = 0;
    }
  }, [entityType, entityId, animationName]);

  // Reset animation when animation name changes
  useEffect(() => {
    setCurrentFrame(0);
    setIsAnimationComplete(false);
    frameCountRef.current = 0;

    // Clear existing interval
    if (animationRef.current) {
      clearInterval(animationRef.current);
      animationRef.current = null;
    }
  }, [animationName]);

  // Handle animation playback
  useEffect(() => {
    if (!frames.length || frames.length === 1 || !isPlaying || isAnimationComplete) return;

    const frameInterval = 1000 / fps;

    const animate = () => {
      setCurrentFrame(prevFrame => {
        const nextFrame = (prevFrame + 1) % frames.length;

        // Check if we've completed a full animation cycle
        if (nextFrame === 0) {
          frameCountRef.current += 1;

          // If not looping and we've gone through the animation once
          if (!loop && frameCountRef.current >= 1) {
            setIsAnimationComplete(true);
            if (onAnimationComplete) {
              onAnimationComplete();
            }
            return prevFrame; // Stay on the last frame
          }
        }

        return nextFrame;
      });
    };

    animationRef.current = setInterval(animate, frameInterval);

    return () => {
      if (animationRef.current) {
        clearInterval(animationRef.current);
      }
    };
  }, [frames, fps, isPlaying, loop, onAnimationComplete, isAnimationComplete]);

  if (!frames.length) {
    return <div className="animated-sprite-loading"></div>;
  }

  // Apply transformations
  const style = {
    transform: `
      scale(${flipX ? -scale : scale}, ${flipY ? -scale : scale})
      rotate(${rotation}deg)
    `,
    transformOrigin: 'center',
  };

  return (
    <div className="animated-sprite">
      <img
        src={frames[currentFrame]}
        alt={`${entityType}-${entityId}`}
        className="sprite-image"
        style={style}
      />
    </div>
  );
};

export default AnimatedSprite;
