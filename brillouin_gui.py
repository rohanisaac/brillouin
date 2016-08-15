#!/usr/bin/env python
"""
description: GUI for folder processing script. Takes folder, spacing and bool
peak crossed value and runs folder process to output csv
author: Rohan Isaac
"""
import Tkinter as tk
import tkFileDialog
import ttk
from brillouin_folder import process_folder

def process(*args):
    # try:
    output.set('Processing folder...')
    folder_value = str(folder.get())
    spacing_value = float(spacing.get())
    crossed_value = bool(crossed.get())
    process_folder(folder_value, spacing_value, crossed_value)
    output.set('Done.')
    #except:
    #    output.set('Error! Check paramters and try again')

def askdirectory(*args):
    folder.set(tkFileDialog.askdirectory())
    output.set('')

root = tk.Tk()
root.title("Brillouin data processing")

mainframe = ttk.Frame(root, padding="3 5 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

folder = tk.StringVar()
spacing = tk.StringVar()
crossed = tk.StringVar()
output = tk.StringVar()

folder_entry = ttk.Entry(mainframe, width=20, textvariable=folder)
spacing_entry = ttk.Entry(mainframe, width=7, textvariable=spacing)


folder_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
spacing_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Label(mainframe, textvariable=output).grid(column=2, row=4, sticky=(tk.W, tk.E))
ttk.Checkbutton(mainframe, text="Peaks crossed?", variable=crossed).grid(column=2, row=3, stick=tk.E)
ttk.Label(mainframe, text="Folder").grid(column=1, row=1, sticky=tk.E)
ttk.Label(mainframe, text="Spacing").grid(column=1, row=2, sticky=tk.E)
ttk.Label(mainframe, text="Status").grid(column=1, row=4, sticky=tk.E)
ttk.Label(mainframe, text="cm").grid(column=3, row=2, sticky=tk.W)
ttk.Button(mainframe, text="Browse", command=askdirectory).grid(column=3, row=1, sticky=tk.E)
ttk.Button(mainframe, text="Process", command=process).grid(column=3, row=5, sticky=tk.W)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

folder_entry.focus()
root.bind('<Return>', process)

root.mainloop()
