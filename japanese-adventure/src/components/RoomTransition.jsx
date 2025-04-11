import { useState, useEffect } from 'react';

const RoomTransition = ({
  isTransitioning,
  fromRoomId,
  toRoomId,
  direction,
  onTransitionComplete
}) => {
  const [transitionPhase, setTransitionPhase] = useState('none'); // 'none', 'fade-out', 'change', 'fade-in'
  const [opacity, setOpacity] = useState(1);

  useEffect(() => {
    if (isTransitioning) {
      // Start transition
      setTransitionPhase('fade-out');

      // Fade out
      let fadeOutTimer = setTimeout(() => {
        setTransitionPhase('change');

        // Change room
        let changeTimer = setTimeout(() => {
          setTransitionPhase('fade-in');

          // Fade in
          let fadeInTimer = setTimeout(() => {
            setTransitionPhase('none');
            if (onTransitionComplete) {
              onTransitionComplete();
            }
          }, 500);

          return () => clearTimeout(fadeInTimer);
        }, 100);

        return () => clearTimeout(changeTimer);
      }, 500);

      return () => clearTimeout(fadeOutTimer);
    }
  }, [isTransitioning, onTransitionComplete]);

  // Update opacity based on transition phase
  useEffect(() => {
    let opacityInterval;

    if (transitionPhase === 'fade-out') {
      opacityInterval = setInterval(() => {
        setOpacity(prevOpacity => {
          const newOpacity = prevOpacity - 0.05;
          return newOpacity <= 0 ? 0 : newOpacity;
        });
      }, 20);
    } else if (transitionPhase === 'fade-in') {
      setOpacity(0);
      opacityInterval = setInterval(() => {
        setOpacity(prevOpacity => {
          const newOpacity = prevOpacity + 0.05;
          return newOpacity >= 1 ? 1 : newOpacity;
        });
      }, 20);
    }

    return () => {
      if (opacityInterval) {
        clearInterval(opacityInterval);
      }
    };
  }, [transitionPhase]);

  // Get transition animation class based on direction
  const getTransitionClass = () => {
    if (!direction || transitionPhase !== 'change') return '';

    switch (direction) {
      case 'north':
        return 'transition-slide-up';
      case 'south':
        return 'transition-slide-down';
      case 'east':
        return 'transition-slide-right';
      case 'west':
        return 'transition-slide-left';
      default:
        return 'transition-fade';
    }
  };

  if (!isTransitioning && transitionPhase === 'none') {
    return null;
  }

  return (
    <div
      className={`room-transition ${getTransitionClass()}`}
      style={{
        opacity: opacity,
        pointerEvents: isTransitioning ? 'auto' : 'none'
      }}
    >
      <div className="transition-content">
        {transitionPhase === 'change' && (
          <div className="transition-message">
            Moving to {toRoomId.replace('_', ' ')}...
          </div>
        )}
      </div>
    </div>
  );
};

export default RoomTransition;
