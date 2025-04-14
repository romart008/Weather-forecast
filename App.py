import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from tkinter import simpledialog
from PIL import Image, ImageTk
from main import city as c

city = simpledialog.askstring("Choose city", "Enter city name: ")

c.city = city
c.parce_weather()
try:
    c.make_graph()
except:
    print("Cant find this city yet...")
    input()
                                                        #ВИГЛЯД
window = tk.Tk()
window.title("Weather")
window.grid(10,10,500,500)
window.resizable(width=False, height=False)

                                                        #ТЕКСТ
city_name = tk.Label(window, 
                   text=f"Weather in {c.city}",
                   height= 2,
                   width= 30,
                   font=("Arial", 42),
                   justify=tk.CENTER
                   )
city_name.grid(column=1,row=0, columnspan= 2)

temp_now = tk.Label(window,
                text=f"Temperature Now: {c.temp_now} °C",
                height= 1,
                width= 30,
                font=("Arial", 24),
                )
temp_now.grid(column=0,row=1,columnspan= 2)

humidity_now = tk.Label(window,
                text=f"Humidity Now: {c.humidity_now} %",
                height= 1,
                width= 30,
                font=("Arial", 24),
                )
humidity_now.grid(column=2,row=1,columnspan= 2)

temp = tk.Label(window,
                text=f"Temperature °C for next 42 hours:",
                font=("Arial", 16),
                )
temp.grid(column=0,row=2, columnspan= 2)

humidity = tk.Label(window,
                text=f"Humidity % for next 42 hours:",
                font=("Arial", 16),
                )
humidity.grid(column=2,row=2, columnspan= 2)

date = tk.Label(window,
                text=f'Data is relevant for {c.date}',
                font=("Arial", 10)
                )
date.grid(row=4,column=0,columnspan=4)

                                                        #ГРАФІКИ
#Температура
tt=Image.open("temp.png")
tt = tt.resize((128*4,96*4))        #Зменшення через те що width і height - обрізають картинку
t =ImageTk.PhotoImage(tt)
imt = tk.Label(window,
               image=t)
imt.image = t
imt.grid(row=3, column=0, columnspan= 2)

#Вологість
hh=Image.open("humidity.png")
hh = hh.resize((128*4,96*4))
h =ImageTk.PhotoImage(hh)
imh = tk.Label(window, 
                image=h)
imh.image = h
imh.grid(row=3, column=2, columnspan= 2)

                                                        #КНОПКИ
style = ttk.Style()
style.configure('TButton', font= ('Arial', 16))

#Імпорт
def load():
    fts = (('Json files', '*.json'),('All files', '*.*'))
    filename = fd.askopenfilename(title='Open a file', initialdir='/',filetypes=fts)
    c.load(filename)
    c.make_graph()
    
    city_name.config(text=f"Weather in {c.city}")
    temp_now.config(text=f"Temperature Now: {c.temp_now} °C")
    humidity_now.config(text=f"Humidity Now: {c.humidity_now} %")
    date.config(text=f'Data is relevant for {c.date}')

    tt=Image.open("temp.png")
    tt = tt.resize((128*4,96*4))
    t =ImageTk.PhotoImage(tt)
    imt.config(image=t)
    imt.image = t

    hh=Image.open("humidity.png")
    hh = hh.resize((128*4,96*4))
    h =ImageTk.PhotoImage(hh)
    imh.config(image=h)
    imh.image = h


open_button = ttk.Button(window,
                        text='Open a File',
                        
                        command=load,
                        )
open_button.grid(row=0,column=0, sticky= 'n')

#Експорт
def export():
    fts = (('Json files', '*.json'),('All files', '*.*'))
    filename = fd.asksaveasfilename(title='Save a file', initialdir='/',filetypes=fts)
    c.export(os.path.abspath(filename))

save_button = ttk.Button(window,
                        text='Save a file',
                        command=export,
                        )
save_button.grid(row=0,column=3, sticky= 'n')

quit = ttk.Button(window,
                  text="Quit",
                  command=window.destroy
                  )
quit.grid(row = 4, column=3, sticky='s')

window.mainloop()