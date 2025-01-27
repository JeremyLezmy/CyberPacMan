
# CyberPunk-Man v2.0

**DISCLAIMER** : I made this game primarly to test DeepSeek R1 performances :smile:
## Overview
**CyberPunk-Man v2.0** is a visually engaging, retro-inspired game built with Python and Pygame. It combines vibrant neon aesthetics with arcade-style gameplay. Navigate the maze, collect dots, avoid ghosts, and progress through levels while enjoying a cyberpunk-themed interface.

## Features
- **Dynamic Gameplay**: Dodge ghosts, collect power pellets, and activate "Power Mode" to chase ghosts for bonus points.
- **Level Selection**: Start your adventure by choosing from different difficulty levels.
- **Animated Cyber UI**: Enjoy glitch text effects, animated grids, and neon-inspired designs.
- **Responsive Controls**: Smooth player movement with keyboard input.
- **Victory and Game Over States**: Visual feedback when you win or lose, including animated confetti effects.
- **Replayability**: Restart the game or progress through challenging levels.

## Requirements
- Python 3.7+
- Pygame 2.0+

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:
   ```bash
   pip install pygame
   ```
3. Ensure the following assets are available in their respective directories:
   - Fonts: `fonts/cyberpunk.ttf` (fallback to `couriernew` if unavailable)
   - Sounds (optional): Add sound effects in the `sounds` directory (e.g., `ui_move.wav`, `ui_select.wav`).

## How to Play
1. Run the game:
   ```bash
   python main.py
   ```
2. Select a level from the menu.
3. Use the arrow keys to control CyberPunk-Man:
   - **Arrow Left**: Move left
   - **Arrow Right**: Move right
   - **Arrow Up**: Move up
   - **Arrow Down**: Move down
4. Collect all dots in the maze to complete the level. Use power pellets to activate "Power Mode" and chase the ghosts!

## Controls
- **Arrow Keys**: Move CyberPunk-Man.
- **ESC**: Quit the game.

## File Structure
- `main.py`: Core game logic.
- `fonts/`: Custom fonts for the cyberpunk theme.
- `sounds/`: Optional sound effects for UI and gameplay.
- `assets/`: Placeholder for additional graphics or assets.

## Known Issues
- Missing assets will fallback to basic fonts or functionality.
- High resource usage on older systems due to animated effects.

## Contributing
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
