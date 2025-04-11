# Japanese Adventure

A text-based language immersion game for learning Japanese through interactive storytelling and exploration.

![Japanese Adventure Game Screenshot](./public/screenshots/game-screenshot.png)

*Note: The screenshot above shows the game interface with Japanese text, romaji transliteration, and English translation.*

## 📖 About

Japanese Adventure is an interactive text-based game designed to help players learn Japanese vocabulary and grammar in a fun, immersive environment. Inspired by classic text adventures like Zork, the game combines storytelling, puzzle-solving, and language learning in a single engaging experience.

Players navigate through different rooms, interact with characters, collect items, and solve puzzles while being exposed to Japanese vocabulary and phrases in context. The game provides both Japanese text (in kanji, hiragana, and katakana), romaji (romanized Japanese), and English translations to support learners at different levels.

## ✨ Features

- **Immersive Text-Based Gameplay**: Explore a virtual world through descriptive text and commands
- **Japanese Language Learning**: Learn vocabulary and phrases in context through gameplay
- **Bilingual Support**: All text is displayed in Japanese, romaji, and English
- **Visual Representations**: ASCII art and visual elements enhance the gaming experience
- **Interactive NPCs**: Talk to characters in Japanese to advance the story
- **Item Collection and Usage**: Find and use items to solve puzzles
- **Vocabulary Tracking**: Track learned Japanese words as you progress
- **Customizable Display**: Toggle between showing/hiding romaji and English translations
- **Sound Effects**: Audio cues enhance the gaming experience
- **Responsive Design**: Play on desktop or mobile devices

## 🚀 Installation

### Prerequisites
- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/itport/japanese-adventure.git
   cd japanese-adventure
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

## 🎮 How to Play

### Basic Commands

Japanese Adventure uses a simple command system. You can enter commands in Japanese, romaji, or English:

| Japanese | Romaji | English | Description |
|----------|--------|---------|-------------|
| 見る | miru | look | Look around or examine an object |
| 行く [方向] | iku [direction] | move [direction] | Move in a direction |
| 取る [物] | toru [object] | take [object] | Pick up an item |
| 置く [物] | oku [object] | drop [object] | Drop an item |
| 持ち物 | mochimono | inventory | Check your inventory |
| [人]と話す | [person] to hanasu | talk to [person] | Talk to an NPC |
| [物]を使う | [mono] o tsukau | use [object] | Use an item |
| ヘルプ | herupu | help | Show available commands |

### Directions

You can move in different directions using these commands:

| Japanese | Romaji | English |
|----------|--------|----------|
| 北 | kita | north |
| 南 | minami | south |
| 東 | higashi | east |
| 西 | nishi | west |
| 上 | ue | up |
| 下 | shita | down |

### Example Commands

```
見る           (Look around the current room)
北に行く        (Move north)
鍵を取る        (Take the key)
ドアを開ける     (Open the door)
お年寄りと話す   (Talk to the old man)
鍵を使う        (Use the key)
持ち物          (Check inventory)
ヘルプ          (Show help)
```

### Game Interface

- **Top Header**: Shows the game title and current room
- **Left Panel**: Displays visual representations of the current room, inventory, and learned vocabulary
- **Right Panel**: Shows game text in Japanese, romaji, and English
- **Bottom Panel**: Command input area where you type your commands

### Language Options

- Use the "Hide English" button to hide English translations for a more immersive experience
- Use the "Hide Romaji" button to challenge yourself with only Japanese text
- Toggle the visual panel on/off for a more text-focused experience

## 🧩 Game Structure

The game consists of several interconnected rooms, each with its own descriptions, items, and NPCs:

- **Starting Room**: Where your adventure begins
- **Living Room**: Contains furniture and possibly NPCs
- **Kitchen**: Find food and drink items
- **Bedroom**: Contains a locked door requiring a key
- **Secret Room**: A hidden area with special items

## 🎯 Learning Goals

Japanese Adventure helps you learn:

1. **Basic Japanese Vocabulary**: Common nouns, verbs, and adjectives
2. **Sentence Structure**: How Japanese sentences are formed
3. **Particle Usage**: Practice with particles like を (o), に (ni), と (to)
4. **Directional Terms**: Learn words for directions and movement
5. **Command Forms**: Practice imperative forms of verbs
6. **Cultural Context**: Learn about Japanese items and concepts

## 🛠️ Technical Details

Japanese Adventure is built with:

- **React**: For the user interface
- **Vite**: For fast development and building
- **CSS**: For styling and animations
- **JavaScript**: For game logic and state management

The game architecture includes:

- **Game Engine**: Handles game state, commands, and logic
- **Parser**: Interprets user commands in multiple languages
- **Data Models**: Defines rooms, items, NPCs, and vocabulary
- **UI Components**: Renders the game interface and visuals

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by classic text adventures like Zork
- Japanese language resources and translations
- Open-source game development community

---

Enjoy your Japanese language adventure! がんばってください！(Ganbatte kudasai! - Good luck!)
