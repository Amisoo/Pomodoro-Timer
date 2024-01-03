import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import ctypes as ct

"""
-Deux carrées a cotes :
    - Un pour le conteur avec un bouton commmencer arreter
          -si le comter n'est pas enclencher on peut regler le minuteur
          - si le comteur est egal ou plus grand que 1 heure alors pause egal 10min (sinon 5 min)
    - un carrer pour le temps passer a reviser (peut etre aussi le temps passer en pause)

     
"""


def dark_title_bar(window):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))


class PomodoroTimer:

    def update_time(self):
        if self.time_left < 0:
            raise "No time no work"
        if self.goal_time_minute > self.time_left:
            self.time_left = self.goal_time_minute
        if self.state == 1:
            self.time_left -= 1
            self.time_label.config(text=f"{self.format_time(self.time_left)} minutes")
            if self.time_left <= 0:
                self.toggle_state()

        self.root.after(1000, self.update_time)
        self.root.after(1000, self.update_goal_time)

    def toggle_state(self):
        if self.state == 0:
            self.state = 1
            self.time_left = self.goal_time_minute * 60
            self.button_text.set("Arreter le Chronomètre")
        elif self.state == 1:
            self.state = 2
            self.button_text.set("Reprendre votre session de concentration")
        elif self.state == 2:
            self.state = 1

            self.button_text.set("Arreter le Chornomètre")
        elif self.time_left <= 0:
            self.time_left = self.time_break * 60
            self.total_time += self.goal_time_minute

    def button(self):
        self.toggle_state()

    def format_time(self, seconds):
        minute_left = int(seconds / 60)
        return f"{minute_left}"

    def up_time(self):
        self.goal_time_minute += 5

    def down_time(self):
        self.goal_time_minute -= 5

    def button_up(self):
        self.up_time()

    def button_down(self):
        self.down_time()

    def update_goal_time(self):
        self.subtitle1.config(text=f" Goal : {self.goal_time_minute} \n Temps restants :")





    def __init__(self):
        self.state = 0
        self.goal_time_minute = 45
        self.time_break = 5
        self.time_left = 0
        self.total_time = 0

        self.root = tk.Tk()
        self.root.geometry("1080x720")
        self.root.minsize(480, 360)
        self.root.title("Pomodoro Timer")
        self.root.tk.call("wm", "iconphoto", self.root._w, PhotoImage(file="logo.png"))
        self.root.config(background='#272727')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        padding_x = 50
        padding_y = 100

        self.frame_minuteur = tk.Frame(self.root, width=200, height=200, bg='#323232')

        self.button_text = tk.StringVar()
        self.button_text.set("Demarrez votre session de concentration")
        button = tk.Button(self.frame_minuteur,
                           textvariable=self.button_text,
                           bg="#848381",
                           fg="black",
                           font=("sans-serif", 15),
                           command=self.button,
                           width=40
                           )
        button.pack(side=tk.BOTTOM)

        button_up = tk.Button(self.frame_minuteur,
                                   text="↑",
                                   bg="#848381",
                                   fg="black",
                                   font=("sans-serif", 20),
                                   command=self.button_up,
                                   width=4,
                                   height=4
                                   )
        button_up.pack(side=tk.RIGHT)

        button_down = tk.Button(self.frame_minuteur,
                                    text="↓ ",
                                    bg="#848381",
                                    fg="black",
                                    font=("sans-serif", 20),
                                    command=self.button_down,
                                    width=4,
                                    height=4
                                    )
        button_down.pack(side=tk.RIGHT)


        self.frame_minuteur.grid(row=0, column=0, padx=(padding_x, padding_x), pady=(padding_y, padding_y),
                                 sticky='nsew')
        self.subtitle1 = tk.Label(self.frame_minuteur, text=f"  Goal : {self.goal_time_minute} \n Temps restants :", font=('sans-serif', 25), bg="#323232",
                                  fg='white')
        self.subtitle1.pack(side=tk.TOP)
        self.time_label = tk.Label(self.frame_minuteur, text=f"{self.goal_time_minute} minutes" , font=("sans-serif", 30),
                                   bg="#323232", fg='white')
        self.time_label.pack(fill=tk.BOTH, expand=1)

        self.frame_temps = tk.Frame(self.root, width=200, height=200, bg='#323232')
        self.frame_temps.grid(row=0, column=1, padx=(padding_x, padding_x), pady=(padding_y, padding_y), sticky="nsew")

        self.subtitle = tk.Label(self.frame_temps, text=f"Temps totals", font=('sans-serif', 25), bg="#323232",
                                 fg='white')
        self.subtitle.pack(side=tk.TOP)

        self.time_total = tk.Label(self.frame_temps, text=f"{self.total_time} minutes", font=('arial', 30),
                                   bg="#323232", fg='white')
        self.time_total.pack(fill=tk.BOTH, expand=1)

        self.root.after(1000, self.update_time)

        dark_title_bar(self.root)

        self.root.mainloop()


PomodoroTimer()

"""
    4 state possible :
    state = 0
     - rien se passe | check
     state = 1
     - study time
         - possible avant tout les states
         - commence lorsque on appuye sur le boutons
         - chronomètre commence
    state = 2
     - break time
        - commence lorsqu'on est en study time et qu'on appuie sur le bouton
        faire arrete le chronomètre
    state = 3  
     - pause time
          -commence seulement apres le state study time 
          - commence lorsque le minuteur est terminé
"""
