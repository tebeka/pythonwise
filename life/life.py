#!/usr/bin/env python

import Tkinter as tk

RUNNING = 0
DEAD, ALIVE = "green", "red"
NUM_ROWS, NUM_COLS = 30, 30
POSITIONS = [(row, col) for row in range(NUM_ROWS) for col in range(NUM_COLS)]
CELLS = {}
ROOT = None
RUN = None

def set_color(position, color):
    cell = CELLS[position]
    cell["background"] = color
    cell["activebackground"] = color

def handler(position):
    def f():
        cell = CELLS[position]
        color = DEAD if cell["background"] == ALIVE else ALIVE
        set_color(position, color)

    return f

def next(cur, step, max):
    return (cur + step) % max

def neighbours(position):
    row, col = position

    urow, drow = (row - 1) % NUM_ROWS, (row + 1) % NUM_ROWS
    lcol, rcol = (col - 1) % NUM_COLS, (col + 1) % NUM_COLS
    return [
        (urow, lcol), (urow, col), (urow, rcol),
        (row, lcol), (row, rcol),
        (drow, lcol), (drow, col), (drow, rcol)
    ]

def is_alive(position):
    return CELLS[position]["background"] == ALIVE

def run():
    if not RUNNING:
        return
    on_step()
    if filter(None, map(is_alive, POSITIONS)):
        ROOT.after(200, run)
    else:
        on_run() # To stop

def on_run():
    global RUNNING

    if RUNNING:
        RUNNING = 0
        RUN["text"] = "Run"
        return

    RUNNING = 1
    RUN["text"] = "Stop"
    run()

def on_step():
    colors = []
    for position in POSITIONS:
        num_alive = len(filter(is_alive, neighbours(position)))
        if is_alive(position):
            color = DEAD if ((num_alive < 2) or (num_alive > 3)) else ALIVE
        else:
            color = ALIVE if (num_alive == 3) else DEAD
        colors.append((position, color))

    map(lambda pc: set_color(*pc), colors)

def on_clear():
    for position in POSITIONS:
        set_color(position, DEAD)

if __name__ == "__main__":
    ROOT = tk.Tk()
    board = tk.Frame(ROOT)
    for row in range(NUM_ROWS):
        r = tk.Frame(board)
        for col in range(NUM_COLS):
            b = tk.Button(r, background=DEAD, activebackground=DEAD,
                          command=handler((row, col)))
            b.pack(side=tk.LEFT)
            CELLS[(row, col)] = b
        r.pack()
    board.pack()
    f = tk.Frame(ROOT)
    RUN = tk.Button(f, command=on_run, text="Run")
    RUN.pack(side=tk.LEFT)
    tk.Button(f, command=on_step, text="Step").pack(side=tk.LEFT)
    tk.Button(f, command=on_clear, text="Clear").pack(side=tk.LEFT)
    f.pack()
    ROOT.bind("<Escape>", lambda e: ROOT.quit())
    ROOT.mainloop()
