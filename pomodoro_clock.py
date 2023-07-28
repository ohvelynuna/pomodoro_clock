import tkinter as tk
import time
from tkinter import messagebox
from tkinter import ttk
from tkinter import font as tkfont
import customtkinter



set_break = 60 * 5 # 5 minutes

class PomodoroClock:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Clock")
        self.work_time = 60 * 25  # 25 minutes
        self.break_time = set_break  # 5 minutes
        self.current_time = self.work_time
        self.banked_break_time = 0
        self.running = False
        self.usingbank = False
        self.break_true = True
        self.timer = None
        self.work_streak = 0
        self.label = customtkinter.CTkLabel(self.master, text=self.time_to_string(self.current_time), font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.label2 = customtkinter.CTkLabel(self.master, text=self.work_streak_statement(self.work_streak), font=("Helvetica", 10))
        self.label2.pack(pady=10)

        self.start_button = customtkinter.CTkButton(self.master, text="Start", command=self.start)
        self.start_button.pack(padx=50, pady=0)

        self.stop_button = customtkinter.CTkButton(self.master, text="Stop", command=self.stop)
        self.stop_button.pack(padx=50, pady=10)

        self.bank_button = customtkinter.CTkButton(self.master, text="Bank", command=self.bank)
        self.bank_button.pack(padx=50, pady=0)

        self.use_bank_button = customtkinter.CTkButton(self.master, text="Use up saved break", command=self.use_bank)
        self.use_bank_button.pack(padx=50, pady=10)

    def time_to_string(self, time):
        minutes = time // 60
        seconds = time % 60
        return f"{minutes:02}:{seconds:02}"
    
    def bank(self):
        if not self.break_true:
            self.banked_break_time += self.current_time
            self.current_time = 1
            messagebox.showinfo(f'Banked', f'You have banked {self.banked_break_time//60}min(s) and {self.banked_break_time%60}sec(s) for your break time!')
        elif self.break_true == True:
            pass
    
    def use_bank(self):
        if self.banked_break_time > 0 and self.break_true == False:
            self.break_true = True
            self.usingbank = True
            self.current_time = 1
        elif self.banked_break_time > 0 and self.break_true == True:
            self.usingbank = True
            self.current_time = 1
            self.break_time = 0

    def work_streak_statement(self, work):
        print("streak", work)
        return f"Your current work streak: {work}"
            
    def update_clock(self):
        if self.running:
            self.current_time -= 1
            self.label.configure(text=self.time_to_string(self.current_time))
            if self.current_time == 0 and self.break_true == True:
                messagebox.showinfo('Time\'s up', 'Time for a break')
                self.break_true = False
                self.current_time += self.break_time
                if self.usingbank == True:
                    self.current_time += self.banked_break_time
                    self.banked_break_time = 0
                    self.break_time = set_break
            if self.current_time == 0 and self.break_true == False:
                if self.usingbank == True:
                    self.usingbank = False
                elif self.usingbank == False:
                    self.work_streak += 1
                    self.label2.configure(text=self.work_streak_statement(self.work_streak))
                print(self.work_streak)
                self.break_true = True
                self.current_time = self.work_time
                messagebox.showinfo('Time\'s up', 'Time for work!')
            self.timer = self.master.after(1000, self.update_clock)

    def start(self):
        if not self.running:
            self.running = True
            self.update_clock()

    def stop(self):
        if self.running:
            self.running = False
            if self.timer is not None:
                self.master.after_cancel(self.timer)
                self.timer = None

root = customtkinter.CTk()
clock = PomodoroClock(root)

root.attributes('-topmost', 1)
root.geometry("250x320")
root.mainloop()
