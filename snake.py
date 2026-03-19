#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ===== Snake – GUI mit abgerundeten Ecken, Highscore und ohne Konsole =====
# Features:
# - Snake-Klassiker auf tkinter Canvas
# - Abgerundetes Fenster (RoundWindow)
# - Highscore-Anzeige oben rechts (lokal in JSON)
# - Themes: Hell / Dunkel (über Startdialog)
# - Wählbare Spielfeldgröße (20x20, 30x30)
# - Geschwindigkeitsstufen (langsam, normal, schnell)
# - Jeder gefressene rote Punkt zählt 1 Punkt
# - Kein Konsolenfenster (automatisch versteckt)

import sys
import ctypes
import json
import os
import random
import tkinter as tk
from tkinter import messagebox

# ------------------------------------------------------------
# Konsole sofort verstecken (für Windows)
# ------------------------------------------------------------
if sys.platform == "win32":
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel32.FreeConsole()

# ------------------------------------------------------------
# Hilfsfunktion für abgerundete Rechtecke (Canvas)
# ------------------------------------------------------------
def _create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
    """Erzeugt ein abgerundetes Rechteck auf einem Canvas."""
    points = [
        x1+r, y1,
        x2-r, y1,
        x2, y1+r,
        x2, y2-r,
        x2-r, y2,
        x1+r, y2,
        x1, y2-r,
        x1, y1+r,
        x1+r, y1  # Rückkehr zum Startpunkt
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_round_rect = _create_round_rect

# ------------------------------------------------------------
# Highscore-Verwaltung
# ------------------------------------------------------------
HIGHSCORE_FILE = "snake_highscores.json"

def load_highscores():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return json.load(f)
    return {"20x20": 0, "30x30": 0}

def save_highscore(size, score):
    highscores = load_highscores()
    key = f"{size}x{size}"
    if score > highscores.get(key, 0):
        highscores[key] = score
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump(highscores, f)
        return True
    return False

# ------------------------------------------------------------
# Custom Fensterklasse mit abgerundeten Ecken
# ------------------------------------------------------------
class RoundWindow:
    TITLE_BAR_HEIGHT = 30  # Höhe der Titelleiste in Pixeln

    def __init__(self, parent=None, width=400, height=350, title="Fenster",
                 bg_color="#ffffff", title_color="#000000", on_close=None):
        """
        Erstellt ein Fenster mit abgerundeten Ecken.
        :param parent: Parent-Fenster (tk.Tk oder tk.Toplevel). Falls None, wird das aktuelle Root verwendet.
        :param on_close: Callback, der beim Schließen des Fensters aufgerufen wird.
        """
        if parent is None:
            parent = tk._default_root
            if parent is None:
                parent = tk.Tk()
                parent.withdraw()  # Root verstecken, falls es neu erstellt wird
        self.root = tk.Toplevel(parent)
        self.root.overrideredirect(True)
        self.root.geometry(f"{width}x{height}+300+200")
        self.root.configure(bg=bg_color)
        self.root.resizable(False, False)
        self.on_close = on_close

        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_round_rect(5, 5, width-5, height-5, r=20, fill=bg_color, outline="#cccccc", width=2)

        # Titelleiste
        title_bar = tk.Frame(self.root, bg=bg_color, height=self.TITLE_BAR_HEIGHT)
        title_bar.place(x=10, y=10, width=width-20)

        title_label = tk.Label(title_bar, text=title, font=("Segoe UI", 10, "bold"),
                               fg=title_color, bg=bg_color)
        title_label.pack(side="left", padx=10)

        close_btn = tk.Button(title_bar, text="✕", font=("Segoe UI", 10, "bold"),
                              fg=title_color, bg=bg_color, bd=0, activebackground="#ffcccc",
                              activeforeground="black", cursor="hand2",
                              command=self.close)
        close_btn.pack(side="right", padx=10)

        # Verschieben
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<B1-Motion>", self.do_move)
        title_label.bind("<ButtonPress-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)

        # Innerer Frame für den Inhalt
        self.inner_frame = tk.Frame(self.root, bg=bg_color)
        # Platzierung abhängig von der Titelleisten-Höhe
        self.inner_frame.place(x=15, y=10 + self.TITLE_BAR_HEIGHT + 5,
                               width=width-30, height=height-20-self.TITLE_BAR_HEIGHT-10)

    def close(self):
        """Schließt das Fenster und ruft ggf. den on_close-Callback auf."""
        if self.on_close:
            self.on_close()
        self.root.destroy()

    def start_move(self, event):
        self.drag_x = event.x_root - self.root.winfo_x()
        self.drag_y = event.y_root - self.root.winfo_y()

    def do_move(self, event):
        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y
        self.root.geometry(f"+{x}+{y}")

# ------------------------------------------------------------
# Snake-Spielklasse (tkinter Canvas)
# ------------------------------------------------------------
class SnakeGame:
    def __init__(self, parent, grid_size=20, speed="normal", theme="light"):
        self.grid_size = grid_size  # Anzahl Zellen pro Seite (z.B. 20)
        self.speed = speed
        self.theme = theme
        self.cell_size = 25  # Pixel pro Zelle
        self.width = self.grid_size * self.cell_size
        self.height = self.grid_size * self.cell_size
        self.win_width = self.width + 60
        self.win_height = self.height + 120

        self.highscore = load_highscores()
        self.highscore_key = f"{grid_size}x{grid_size}"

        # Fenster erstellen (mit on_close, um ggf. das Hauptprogramm zu beenden)
        self.win = RoundWindow(parent, self.win_width, self.win_height,
                               f"Snake {grid_size}x{grid_size}",
                               bg_color=self._bg(), title_color=self._fg(),
                               on_close=self.on_window_close)
        self.root = self.win.root
        self.inner = self.win.inner_frame

        # Spielfeld Canvas
        self.canvas = tk.Canvas(self.inner, width=self.width, height=self.height,
                                bg=self._canvas_bg(), highlightthickness=0)
        self.canvas.pack(pady=10)

        # Statusleiste (Score links, Highscore rechts)
        status_frame = tk.Frame(self.inner, bg=self.inner.cget('bg'))
        status_frame.pack(fill="x", padx=10, pady=5)

        self.score_label = tk.Label(status_frame, text="Score: 0", font=("Segoe UI", 12),
                                     bg=self.inner.cget('bg'), fg=self._fg())
        self.score_label.pack(side="left")

        highscore_val = self.highscore.get(self.highscore_key, 0)
        self.highscore_label = tk.Label(status_frame, text=f"Highscore: {highscore_val}",
                                         font=("Segoe UI", 12), bg=self.inner.cget('bg'), fg=self._fg())
        self.highscore_label.pack(side="right")

        # Neustart-Button
        restart_btn = tk.Button(self.inner, text="Neustart", font=("Segoe UI", 10, "bold"),
                                 command=self.restart, bg="#FFB74D", fg="black", bd=0,
                                 padx=15, pady=5, cursor="hand2")
        restart_btn.pack(pady=5)

        # Tastatursteuerung
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.focus_set()

        # Spielvariablen
        self.reset_game()

        # Geschwindigkeit
        self.speed_map = {"langsam": 200, "normal": 150, "schnell": 100}
        self.delay = self.speed_map.get(speed, 150)

        # Spielschleife starten
        self.game_loop()

    def on_window_close(self):
        """Wird aufgerufen, wenn das Spiel-Fenster geschlossen wird.
        Beendet das Hauptprogramm, indem das Root-Fenster zerstört wird."""
        # Das Haupt-Root-Fenster (versteckt) zerstören, um mainloop zu beenden
        if tk._default_root:
            tk._default_root.quit()
            tk._default_root.destroy()

    def _bg(self):
        return "#ffffff" if self.theme == "light" else "#2d2d2d"

    def _fg(self):
        return "#000000" if self.theme == "light" else "#ffffff"

    def _canvas_bg(self):
        return "#f0f0f0" if self.theme == "light" else "#1e1e1e"

    def _snake_color(self):
        return "#4CAF50" if self.theme == "light" else "#2e7d32"

    def _food_color(self):
        return "#FF5252" if self.theme == "light" else "#d32f2f"

    def reset_game(self):
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]  # Start in der Mitte
        self.direction = (1, 0)  # Anfangs nach rechts (x, y)
        self.next_direction = (1, 0)
        self.food = self.place_food()
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.update_score()
        self.draw()

    def place_food(self):
        """Setzt das Essen an eine freie Stelle. Gibt None zurück, wenn keine freie Zelle existiert."""
        free_cells = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)
                      if (x, y) not in self.snake]
        if not free_cells:
            return None  # Kein freier Platz mehr -> Sieg
        return random.choice(free_cells)

    def draw(self):
        self.canvas.delete("all")
        # Gitter zeichnen (optional)
        for i in range(self.grid_size):
            self.canvas.create_line(0, i * self.cell_size, self.width, i * self.cell_size, fill="#cccccc", width=1)
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.height, fill="#cccccc", width=1)

        # Schlange zeichnen (Kopf etwas heller)
        for idx, (x, y) in enumerate(self.snake):
            color = self._snake_color() if idx == 0 else self._snake_color()
            self.canvas.create_rectangle(x * self.cell_size + 2, y * self.cell_size + 2,
                                          (x + 1) * self.cell_size - 2, (y + 1) * self.cell_size - 2,
                                          fill=color, outline="")
        # Essen zeichnen, falls vorhanden
        if self.food:
            fx, fy = self.food
            self.canvas.create_oval(fx * self.cell_size + 4, fy * self.cell_size + 4,
                                     (fx + 1) * self.cell_size - 4, (fy + 1) * self.cell_size - 4,
                                     fill=self._food_color(), outline="")

        # Pause-Anzeige
        if self.paused:
            # Halbtransparenter Effekt durch Rechteck mit Stippling
            self.canvas.create_rectangle(0, 0, self.width, self.height,
                                         fill="gray", stipple="gray50", outline="")
            self.canvas.create_text(self.width // 2, self.height // 2,
                                    text="PAUSE", font=("Segoe UI", 24, "bold"),
                                    fill="white")

    def move_snake(self):
        if self.game_over or self.paused:
            return

        # Richtung übernehmen (keine 180-Grad-Wende)
        if (self.next_direction[0] != -self.direction[0] or self.next_direction[1] != -self.direction[1]):
            self.direction = self.next_direction

        # Neuen Kopf berechnen
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Kollision mit Wänden? (Spiel vorbei)
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size):
            self.game_over = True
            self.game_over_sequence()
            return

        # Kollision mit sich selbst?
        if new_head in self.snake:
            self.game_over = True
            self.game_over_sequence()
            return

        # Fressen?
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += 1
            self.food = self.place_food()
            # Prüfen, ob kein Essen mehr platziert werden kann (Sieg)
            if self.food is None:
                self.game_won = True
                self.game_over_sequence(won=True)
                return
            # Highscore während des Spiels aktualisieren
            if self.score > self.highscore.get(self.highscore_key, 0):
                self.highscore[self.highscore_key] = self.score
                self.highscore_label.config(text=f"Highscore: {self.score}")
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

        self.update_score()
        self.draw()

    def game_over_sequence(self, won=False):
        # Highscore speichern (nur wenn nicht gewonnen? Auch bei Sieg sollte Highscore gespeichert werden)
        is_new = save_highscore(self.grid_size, self.score)
        self.highscore = load_highscores()
        highscore_val = self.highscore.get(self.highscore_key, 0)
        self.highscore_label.config(text=f"Highscore: {highscore_val}")

        if won:
            msg = f"🎉 Glückwunsch! Du hast das gesamte Feld gefüllt!\nDein Score: {self.score}\n"
        else:
            msg = f"Game Over! Dein Score: {self.score}\n"
        if is_new:
            msg += "🎉 Neuer Highscore!"
        messagebox.showinfo("Spielende", msg)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def on_key_press(self, event):
        key = event.keysym
        if key == "Up":
            self.next_direction = (0, -1)
        elif key == "Down":
            self.next_direction = (0, 1)
        elif key == "Left":
            self.next_direction = (-1, 0)
        elif key == "Right":
            self.next_direction = (1, 0)
        elif key == "space":
            self.paused = not self.paused
            self.draw()  # Sofort Pause-Status anzeigen
        elif key == "r" or key == "R":
            self.restart()

    def restart(self):
        self.reset_game()
        self.highscore = load_highscores()
        highscore_val = self.highscore.get(self.highscore_key, 0)
        self.highscore_label.config(text=f"Highscore: {highscore_val}")

    def game_loop(self):
        self.move_snake()
        self.root.after(self.delay, self.game_loop)

# ------------------------------------------------------------
# Startdialog
# ------------------------------------------------------------
def start_dialog(parent):
    win = RoundWindow(parent, 400, 350, "Snake – Einstellungen",
                      bg_color="#ffffff", title_color="#000000")
    root = win.root
    inner = win.inner_frame

    tk.Label(inner, text="🐍 Snake", font=("Segoe UI", 16, "bold"),
             bg=inner.cget('bg'), fg="black").pack(pady=10)

    # Größenauswahl
    size_frame = tk.Frame(inner, bg=inner.cget('bg'))
    size_frame.pack(pady=5)
    tk.Label(size_frame, text="Spielfeldgröße:", font=("Segoe UI", 10),
             bg=inner.cget('bg'), fg="black").pack(side="left", padx=5)

    size_var = tk.StringVar(value="20")
    rb_20 = tk.Radiobutton(size_frame, text="20x20", variable=size_var, value="20",
                           bg=inner.cget('bg'), fg="black", selectcolor="white")
    rb_20.pack(side="left", padx=2)
    rb_30 = tk.Radiobutton(size_frame, text="30x30", variable=size_var, value="30",
                           bg=inner.cget('bg'), fg="black", selectcolor="white")
    rb_30.pack(side="left", padx=2)

    # Geschwindigkeit
    speed_frame = tk.Frame(inner, bg=inner.cget('bg'))
    speed_frame.pack(pady=5)
    tk.Label(speed_frame, text="Geschwindigkeit:", font=("Segoe UI", 10),
             bg=inner.cget('bg'), fg="black").pack(side="left", padx=5)

    speed_var = tk.StringVar(value="normal")
    rb_slow = tk.Radiobutton(speed_frame, text="Langsam", variable=speed_var, value="langsam",
                              bg=inner.cget('bg'), fg="black", selectcolor="white")
    rb_slow.pack(side="left", padx=2)
    rb_normal = tk.Radiobutton(speed_frame, text="Normal", variable=speed_var, value="normal",
                                bg=inner.cget('bg'), fg="black", selectcolor="white")
    rb_normal.pack(side="left", padx=2)
    rb_fast = tk.Radiobutton(speed_frame, text="Schnell", variable=speed_var, value="schnell",
                              bg=inner.cget('bg'), fg="black", selectcolor="white")
    rb_fast.pack(side="left", padx=2)

    # Theme
    theme_frame = tk.Frame(inner, bg=inner.cget('bg'))
    theme_frame.pack(pady=5)
    tk.Label(theme_frame, text="Theme:", font=("Segoe UI", 10),
             bg=inner.cget('bg'), fg="black").pack(side="left", padx=5)

    theme_var = tk.StringVar(value="light")
    rb_light = tk.Radiobutton(theme_frame, text="Hell", variable=theme_var, value="light",
                               bg=inner.cget('bg'), fg="black", selectcolor="white")
    rb_light.pack(side="left", padx=2)
    rb_dark = tk.Radiobutton(theme_frame, text="Dunkel", variable=theme_var, value="dark",
                              bg=inner.cget('bg'), fg="black", selectcolor="white")
    rb_dark.pack(side="left", padx=2)

    # Highscore-Vorschau
    highscores = load_highscores()
    hs_text = f"Aktuelle Highscores:\n20x20: {highscores['20x20']}\n30x30: {highscores['30x30']}"
    tk.Label(inner, text=hs_text, font=("Segoe UI", 9), justify="left",
             bg=inner.cget('bg'), fg="black").pack(pady=10)

    def start_game():
        size = int(size_var.get())
        speed = speed_var.get()
        theme = theme_var.get()
        win.close()  # Dialog schließen
        # Spiel starten (mit demselben Parent)
        SnakeGame(parent, size, speed, theme)

    tk.Button(inner, text="Spiel starten", font=("Segoe UI", 11, "bold"),
              command=start_game, bg="#4CAF50", fg="white", bd=0,
              padx=20, pady=5, cursor="hand2").pack(pady=10)

    # Warten, bis der Dialog geschlossen wird (blockiert nicht die Hauptschleife)
    root.wait_window()

if __name__ == "__main__":
    # Einmaliges Root-Fenster erstellen und verstecken
    root = tk.Tk()
    root.withdraw()

    # Startdialog anzeigen (blockiert bis zum Schließen)
    start_dialog(root)

    # Hauptschleife starten – läuft, bis das Spiel-Fenster geschlossen wird
    root.mainloop()
