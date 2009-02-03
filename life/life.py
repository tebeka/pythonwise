#!/usr/bin/env python

import Tkinter as tk

DEAD = "green"
ALIVE = "red"
NUM_ROWS = 10
NUM_COLS = 10

CELLS = []
def handler(row, col):
    def f():
        cell = CELLS[row][col]
        color = DEAD if cell["background"] == ALIVE else ALIVE
        cell["background"] = color
        cell["activebackground"] = color


    return f

def run():
    pass

def step():
    pass

def clear():
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            CELLS[row][col]["background"] = DEAD

root = tk.Tk()
board = tk.Frame(root)
for row in range(NUM_ROWS):
    r = tk.Frame(board)
    cells = []
    for col in range(NUM_COLS):
        b = tk.Button(r, background=DEAD, activebackground=DEAD,
                      command=handler(row, col))
        b.pack(side=tk.LEFT)
        cells.append(b)
    r.pack()
    CELLS.append(cells)
board.pack()
f = tk.Frame(root)
tk.Button(f, command=run, text="Run").pack(side=tk.LEFT)
tk.Button(f, command=step, text="Step").pack(side=tk.LEFT)
tk.Button(f, command=clear, text="Clear").pack(side=tk.LEFT)
f.pack()
root.mainloop()
