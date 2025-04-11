import { useState } from 'react';

const CommandInput = ({ onSubmit }) => {
  const [command, setCommand] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (command.trim()) {
      onSubmit(command);
      setCommand('');
    }
  };

  return (
    <div className="command-input">
      <form onSubmit={handleSubmit}>
        <div className="input-container">
          <span className="prompt">&gt;</span>
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="Type your command..."
            autoFocus
          />
        </div>
        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>
    </div>
  );
};

export default CommandInput;
