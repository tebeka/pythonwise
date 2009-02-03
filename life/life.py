#!/usr/bin/env python

import Tkinter as tk

DEAD = "green"
ALIVE = "red"
NUM_ROWS = 10
NUM_COLS = 10
INDEXES = [(row, col) for row in range(NUM_ROWS) for col in range(NUM_COLS)]
CELLS = {}

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

def is_in_board(position):
    row, col = position
    return (0 <= row < NUM_ROWS) and (0 <= col < NUM_COLS)

def neighbours(position):
    row, col = position
    candidates = [
        [row - 1, col -1], [row - 1, col], [row - 1, col + 1],
        [row, col - 1], [row, col + 1],
        [row + 1, col - 1], [row +1, col], [row +1, col + 1]
    ]

    return filter(is_in_board, candidates)

def is_alive(position):
    return CELLS[position]["background"] == ALIVE

def run():
    pass

def copy_state():
    pass

def step():
    board = []
    for position in INDEXES:
        num_alive = len(filter(is_alive, neighbours(position)))
        if is_alive(position):
            color = DEAD if ((num_alive < 2) or (num_alive > 3)) else ALIVE
        else:
            color = ALIVE if (num_alive == 3) else DEAD

        set_color(position, color)


def clear():
    for position in INDEXES:
        set_color(position, DEAD)

root = tk.Tk()
board = tk.Frame(root)
for row in range(NUM_ROWS):
    r = tk.Frame(board)
    for col in range(NUM_COLS):
        b = tk.Button(r, background=DEAD, activebackground=DEAD,
                      command=handler((row, col)))
        b.pack(side=tk.LEFT)
        CELLS[(row, col)] = b
    r.pack()
board.pack()
f = tk.Frame(root)
tk.Button(f, command=run, text="Run").pack(side=tk.LEFT)
tk.Button(f, command=step, text="Step").pack(side=tk.LEFT)
tk.Button(f, command=clear, text="Clear").pack(side=tk.LEFT)
f.pack()
root.bind("<Escape>", lambda e: root.quit())
root.mainloop()
