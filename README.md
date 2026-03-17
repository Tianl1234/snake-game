# 🐍 Snake Game with Rounded Corners & Highscore

A classic Snake game implemented in Python using `tkinter`. It features a modern, rounded‑corner window, a persistent highscore system, multiple themes, and adjustable speed and grid size – all without a console window.

---

## ✨ Features

- **Rounded window** – smoothly rounded corners with a custom title bar (drag to move).  
- **Highscore** – your best score is saved locally in `snake_highscores.json`.  
- **Themes** – choose between **Light** and **Dark** mode before starting.  
- **Grid sizes** – play on a **20×20** or **30×30** board.  
- **Speed levels** – select **slow**, **normal**, or **fast** to adjust the game’s pace.  
- **No console window** – the terminal is automatically hidden (even without `.pyw`).  
- **Keyboard controls** – arrow keys to move, space to pause, `R` to restart.  
- **Score display** – current score on the left, highscore on the right.  

---

## 📦 Requirements

- **Python 3.6 or higher** (tested with 3.10–3.13).  
- **tkinter** – comes with Python on Windows, macOS, and most Linux distributions.  
- No additional libraries are needed.

---

## 🚀 How to Run

1. **Save the script** as `snake.py` (or any name you like).  
2. **Double‑click** the file – the start dialog opens immediately.  
3. Choose your preferred settings (grid size, speed, theme) and click **“Spiel starten”** (Start game).  
4. Use the **arrow keys** to control the snake.  
5. Press **space** to pause/resume, or **R** to restart.  

> 💡 The console window is hidden automatically, so the game runs quietly in the background.

---

## 🎮 How to Play

- The snake starts in the middle of the board and moves continuously.  
- Eat the **red food** to grow and increase your score by **1 point**.  
- Avoid hitting the **walls** or the **snake’s own body** – doing so ends the game.  
- Try to achieve the highest score possible!  

---

## 🧠 Highscore System

- Your best score for each grid size is saved locally in `snake_highscores.json`.  
- During the game, the **highscore label** updates immediately if you beat the record.  
- After a game over, you’ll see a message box with your final score and whether you set a new highscore.  

---

## 🛠️ Customisation

### Themes
You can switch between **Light** (white background) and **Dark** (dark grey background) in the start dialog.

### Speed
Three speeds are available:
- **Langsam** (slow) – 200 ms per move  
- **Normal** – 150 ms per move  
- **Schnell** (fast) – 100 ms per move  

### Grid Size
- **20×20** – smaller board, faster games.  
- **30×30** – larger board, more room to manoeuvre.

---

## 🐛 Troubleshooting

| Problem | Solution |
|--------|----------|
| **Nothing happens when I double‑click** | Make sure Python is installed. Open a terminal and run `python --version`. If that works, run the script from the terminal with `python snake.py` to see error messages. |
| **The window appears but has no title bar** | The custom title bar is part of the design – you can still drag the window by clicking the title text or the bar itself. |
| **The game is too fast / too slow** | Adjust the speed in the start dialog. You can also change the `self.delay` values in the code. |
| **Highscore file is missing** | It will be created automatically after you finish your first game. |
| **I want to reset the highscore** | Delete the `snake_highscores.json` file – it will be recreated with zero scores. |

---

## 📄 License

This project is open‑source and free to use. No warranty.

---

Enjoy the game and try to beat your own highscore! 🎉
