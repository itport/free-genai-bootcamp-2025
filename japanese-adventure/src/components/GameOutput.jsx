import { useState } from 'react';

const GameOutput = ({ gameLog }) => {
  const [showTranslation, setShowTranslation] = useState(true);
  const [showRomaji, setShowRomaji] = useState(true);

  const toggleTranslation = () => {
    setShowTranslation(!showTranslation);
  };

  const toggleRomaji = () => {
    setShowRomaji(!showRomaji);
  };

  return (
    <div className="game-output">
      <div className="translation-toggle">
        <button onClick={toggleTranslation}>
          {showTranslation ? 'Hide English' : 'Show English'}
        </button>
        <button onClick={toggleRomaji}>
          {showRomaji ? 'Hide Romaji' : 'Show Romaji'}
        </button>
      </div>

      <div className="game-messages">
        {gameLog.map((entry) => (
          <div key={entry.id} className="message-entry">
            <div className="japanese-text">{entry.message.japanese}</div>
            {showRomaji && entry.message.romaji && (
              <div className="romaji-text">{entry.message.romaji}</div>
            )}
            {showTranslation && (
              <div className="english-text">{entry.message.english}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default GameOutput;
