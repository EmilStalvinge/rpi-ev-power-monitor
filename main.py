#!/usr/bin/env python3
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.ttk import Button
from tkinter import ttk
import os
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#os.system('sudo poweroff')


current_list=[0]*20
voltage_list=[0]*20

done = False

while not done:
    done = True
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, address = 0x48)

        #ads.gain = 16

        chan_current = AnalogIn(ads, ADS.P2)
        chan_voltage = AnalogIn(ads, ADS.P1)
    except:
        print("no i2c device on inilialize")
        done = False

os.environ.__setitem__('DISPLAY', ':0.0')
gui = tk.Tk()
gui.attributes('-fullscreen', True)
gui.configure(bg="black")

s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', bordercolor ='black', darkcolor='black', lightcolor = 'black', troughcolor = 'black')
s.configure("blue.Horizontal.TProgressbar", foreground='#350', background='#345', bordercolor ='black', darkcolor='black', lightcolor = 'black', troughcolor = 'black')
s.configure("green.Horizontal.TProgressbar", foreground='green', background='green',  bordercolor ='black', darkcolor='black', lightcolor = 'black', troughcolor = 'black')
s.configure('W.TButton', background='black', foreground='white', font=('Arial', 24 ), bordercolor ='white', darkcolor='black', lightcolor = 'black', troughcolor = 'black')

def helloCallBack():
   print("shut down recieved")
   os.system('sudo poweroff')


#### text ######
voltage_txt = tk.Label(gui, text="V", width = 10,
		 font = "Times 32", bg = "black", fg ="white")
voltage_txt.grid(column = 1, row = 0, ipady = 20, pady = 20, padx = 20)

current_txt = tk.Label(gui, text="0 A", width = 10,
                 font = "Times 32", bg = "black", fg ="white")
current_txt.grid(column = 1, row = 1, ipady = 20, pady = 20, padx = 20)

power_txt = tk.Label(gui, text="0 W", width = 10,
                 font = "Times 32", bg = "black", fg ="white")
power_txt.grid(column = 1, row = 2, ipady = 20, pady = 20, padx = 20)

#mytxt.grid(row=1, column =0, sticky = 'news')

# Progress bar widget

voltage_bar = Progressbar(gui, orient = "horizontal",
		   length = 400, mode = 'determinate', style="blue.Horizontal.TProgressbar")
voltage_bar.grid(column=0, row=0, ipady = 20, pady = 20, padx = 30)

current_bar = Progressbar(gui, orient = "horizontal",
              length = 400, mode = 'determinate', style="red.Horizontal.TProgressbar")
current_bar.grid(column=0, row=1, ipady = 20, pady = 20, padx = 30)

power_bar = Progressbar(gui, orient = "horizontal",
              length = 400, mode = 'determinate', style="green.Horizontal.TProgressbar")
power_bar.grid(column=0, row=2, ipady = 20, pady = 20, padx = 30)

button = Button(gui, text ="Off", command = helloCallBack, style='W.TButton')
button.grid(column=0, row=3, ipady = 5, pady = 20, padx = 20)


# Function responsible for the updation
# of the progress bar value
def bar():
    import time

#bar()

def avg_current(current):
   current_list.pop(-1)
   current_list.insert(0,current)
   return sum(current_list)/20

def avg_voltage(current):
   voltage_list.pop(-1)
   voltage_list.insert(0,current)
   return sum(voltage_list)/20

def update_bar():

    voltage = -1.0
    current = -1.0
    try:
        voltage = chan_voltage.value/237.2
        current = (chan_current.value+10)/38.8
    except:
        print("no i2c device")

    gui.update_idletasks()

    average_voltage = avg_voltage(voltage) 
    voltage_bar['value'] = (average_voltage - 88.8) *(100/(100.8-88.8))
    voltage_txt.config(text = str(round(average_voltage,1))+ " V")

    average_current = avg_current(current) 
    current_txt.config(text = str(round(average_current)) + " A")
    current_bar['value'] = average_current/3 #scale o-100

    power = average_voltage*average_current
    power_txt.config(text = str(round(power/1000)) + " kW") 
    power_bar['value'] = power/300 #scale o-100
    

    gui.after(50, update_bar)





if __name__ == '__main__':
    pass
    gui.after(50, update_bar)
    gui.mainloop()

