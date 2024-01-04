import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import ctypes as ct
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class PomodoroTimer:

    def update_time(self):
        if self.time_left < 0:
            raise "No time no work"
        if self.goal_time_minute > self.time_left:
            self.time_left = self.goal_time_minute
        if self.state == 1:
            self.time_left -= 1
            self.time_label.configure(text=f"{self.format_time(self.time_left)} minutes")
            if self.time_left <= 0:
                self.toggle_state()

        self.root.after(1000, self.update_time)
        self.root.after(1000, self.update_goal_time)

    def toggle_state(self):
        if self.state == 0:
            self.state = 1
            self.time_left = self.goal_time_minute * 60
            self.button_text.set("◼")
        elif self.state == 1:
            self.state = 2
            self.button_text.set("▶ Reprendre la session")
        elif self.state == 2:
            self.state = 1

            self.button_text.set("◼")
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
        self.subtitle1.configure(text=f" Goal : {self.goal_time_minute} \n Temps restants :")





    def __init__(self):
        self.state = 0
        self.goal_time_minute = 45
        self.time_break = 5
        self.time_left = 0
        self.total_time = 0



        self.root = customtkinter.CTk()
        self.root.geometry("1080x720")
        self.root.minsize(480, 360)
        self.root.title("Pomodoro Timer")
        self.root.tk.call("wm", "iconphoto", self.root._w, PhotoImage(file="logo.png"))
        self.root.configure(background='#272727')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        padding_x = 50
        padding_y = 100

        self.frame_minuteur = customtkinter.CTkFrame(master=self.root, corner_radius=20)
        self.frame_minuteur.grid(row=0, column=0, padx=(padding_x, padding_x), pady=(padding_y, padding_y),
                                 sticky='nsew')

        self.button_text = tk.StringVar()
        self.button_text.set("▶ Demarrez votre session de concentration")
        button = customtkinter.CTkButton(master=self.frame_minuteur,
                           textvariable=self.button_text,
                            font=("Roboto", 27),
                           command=self.button,
                           width=150,
                           height=50,
                            fg_color="#848381",
                            text_color="black"

                           )
        button.pack(side=tk.BOTTOM)

        button_up = customtkinter.CTkButton(master=self.frame_minuteur,
                                   text="↑",
                                   font=("Roboto", 25),
                                   command=self.button_up,
                                   width=75,
                                   height=175,
                                   fg_color="#848381",
                                    text_color='black'
                                   )
        button_up.pack(side=tk.RIGHT)

        button_down = customtkinter.CTkButton(master=self.frame_minuteur,
                                    text="↓ ",
                                    font=("Roboto", 25),
                                    command=self.button_down,
                                    width=75,
                                    height=175,
                                    fg_color="#848381",
                                    text_color='black'
                                    )
        button_down.pack(side=tk.RIGHT)



        self.subtitle1 = customtkinter.CTkLabel(master=self.frame_minuteur, text=f"  Goal : {self.goal_time_minute} minutes \n Temps restants :", font=('Roboto', 25))

        self.subtitle1.pack(side=tk.TOP, pady=15)
        self.time_label = customtkinter.CTkLabel(master=self.frame_minuteur, text=f"{self.goal_time_minute} minutes", font=('Roboto', 30)
                                   )
        self.time_label.pack(fill=tk.BOTH, expand=1)

        self.frame_temps = customtkinter.CTkFrame(master=self.root, width=200, height=200, corner_radius=20)
        self.frame_temps.grid(row=0, column=1, padx=(padding_x, padding_x), pady=(padding_y, padding_y), sticky="nsew")



        self.subtitle = customtkinter.CTkLabel(master=self.frame_temps, text=f"Temps totals", font=('sans-serif', 25)
                                 )
        self.subtitle.pack(pady=15)




        self.time_total = customtkinter.CTkLabel(master=self.frame_temps, text=f"{self.total_time} minutes", font=('arial', 30),corner_radius=20
                                )
        self.time_total.pack(expand=True)
        self.frame_temps.pack_propagate(False)

        self.root.after(1000, self.update_time)


        self.root.mainloop()

if __name__ == "__main__":
    PomodoroTimer()
