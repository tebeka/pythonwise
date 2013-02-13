#!/usr/bin/env python
'''Quick and dirtry program to provide a UI for converting PDF to JPEG (using
ImageMagick's "convert"
'''

from sys import version_info

if version_info[0] > 2:
    import tkinter as tk
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showerror, showinfo
else:
    import Tkinter as tk
    from tkFileDialog import askopenfilename
    from tkMessageBox import showerror, showinfo
from subprocess import check_call, CalledProcessError
from os.path import isfile, splitext

def select_file(entry):
    '''Select a file into entry'''
    filename = askopenfilename()
    if not filename:
        return

    entry.delete(0, tk.END)
    entry.insert(0, filename)

def convert(pdf):
    '''Convert a PDF to JPG'''
    if not isfile(pdf):
        showerror("ERROR", "Can't find {0}".format(pdf))
        return

    jpg = splitext(pdf)[0] + ".jpg"

    try:
        check_call(["convert", "-quality", "100%", pdf, jpg])
        showinfo("Converted", "{0} converted".format(pdf))
    except (OSError, CalledProcessError) as e:
        showerror("ERROR", "ERROR: {0}".format(e))

def main():
    root = tk.Tk()
    root.title("PDF to JPEG converter")

    # PDF File: _________________ [...]
    frame = tk.Frame(root)
    tk.Label(frame, text="PDF File:").pack(side=tk.LEFT)
    pdf = tk.Entry(frame, width=60)
    pdf.pack(side=tk.LEFT)
    tk.Button(frame, text="...",
              command=lambda: select_file(pdf)).pack(side=tk.LEFT)
    frame.pack()

    # [Convert] [Quit]
    frame = tk.Frame(root)
    tk.Button(frame, text="Convert",
              command=lambda: convert(pdf.get())).pack(side=tk.LEFT)
    tk.Button(frame, text="Quit", command=root.quit).pack(side=tk.LEFT)
    frame.pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    main()

