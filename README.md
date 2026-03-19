# Snake Game with Rounded Corners and Highscore

A classic Snake game implemented in Python using Tkinter, featuring a custom rounded window, highscore persistence, theme selection, and adjustable game speed. No console window appears on Windows (when run as `.pyw`).

## Features

- **Classic Snake gameplay** – Eat red food pellets, grow longer, avoid walls and yourself.
- **Rounded window** – A custom non‑rectangular window with a draggable title bar.
- **Highscore storage** – Local JSON file saves your best scores per grid size.
- **Multiple grid sizes** – Choose between 20×20 and 30×30.
- **Speed levels** – Slow, normal, or fast game speed.
- **Light and Dark themes** – Select your preferred color scheme before starting.
- **Pause function** – Press `Space` to pause/resume.
- **Restart** – Press `R` or click the restart button.
- **Game‑won detection** – If you fill the entire grid, you win!
- **No console window** – Automatically hidden on Windows; use `.pyw` on other platforms.

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- No additional packages required

## Installation / Running

1. **Clone or download** the script (e.g., `snake_game.py`).
2. **Run the script**:
   - On Windows, you can simply double‑click the file (if Python is associated with `.py` files) or run it from the command line:
python snake_game.py

text
- To hide the console window on Windows, rename the file to `snake_game.pyw` and double‑click it.
- On Linux/macOS, run it from the terminal:
python3 snake_game.py

text
The game will start with a settings dialog.

## How to Play

- **Arrow keys** – Move the snake (Up, Down, Left, Right).
- **Space** – Pause / Resume the game.
- **R** – Restart the game at any time.
- **Close button** – Exit the game.

The goal is to eat the red food pellets. Each pellet increases your score by 1. The game ends if the snake hits the wall or its own body. If you manage to fill the entire grid, you win!

## Highscores

Highscores are stored in a file named `snake_highscores.json` in the same directory as the script. The file is created automatically and contains the best scores for each grid size.

## Customization

You can change the game settings in the start dialog:
- **Grid size** – 20×20 or 30×30.
- **Speed** – Langsam (slow), Normal, Schnell (fast).
- **Theme** – Hell (light) or Dunkel (dark).

## Troubleshooting

- **Game window does not appear** – Make sure you have Python and Tkinter installed. On some Linux distributions you may need to install `python3-tk` separately.
- **Console window still shows on Windows** – Rename the file to `.pyw` or run it with `pythonw.exe` (if available).
- **Highscore file not created** – The script needs write permissions in its directory. Run it from a location where you have write access.
