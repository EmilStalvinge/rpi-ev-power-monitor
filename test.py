#!/usr/bin/env python3
import tkinter as tk
from tkinter.ttk import Progressbar
import os


os.environ.__setitem__('DISPLAY', ':0.0')
gui = tk.Tk()
gui.attributes('-fullscreen', True)
gui.configure(bg="black")

#### text ######
voltage_txt = tk.Label(gui, text="V", width = 10,
		 font = "Times 32", bg = "black", fg ="white")
current_txt = tk.Label(gui, text="0 A", width = 10,
                 font = "Times 32", bg = "black", fg ="white")
voltage_txt.grid(column = 1, row = 0, ipady = 30, pady = 30, padx = 30)
current_txt.grid(column = 1, row = 1, ipady = 30, pady = 30, padx = 30)

#mytxt.grid(row=1, column =0, sticky = 'news')

# Progress bar widget
current_bar = Progressbar(gui, orient = "horizontal",
              length = 400, mode = 'determinate')
current_bar.grid(column=0, row=1, ipady = 30, pady = 30, padx = 30)

voltage_bar = Progressbar(gui, orient = "horizontal",
		   length = 400, mode = 'determinate')
voltage_bar.grid(column=0, row=0, ipady = 30, pady = 30, padx = 30)

# Function responsible for the updation
# of the progress bar value
def bar():
    import time

#bar()

def avg_current(current):
   current_list.pop(-1)
   current_list.insert(0,current)
   return sum(current_list)/20
def update_bar():
    voltage_bar['value'] = 100
    current_bar['value'] = 33
    gui.update_idletasks()
    voltage_txt.config(text = str(100) + " V")
    current_txt.config(text = str(33) + " A")
    gui.after(50, update_bar)

if __name__ == '__main__':
    gui.after(50, update_bar)
    gui.mainloop()

