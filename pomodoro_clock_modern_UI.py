import tkinter as tk
import time
from tkinter import messagebox
from tkinter import ttk
from tkinter import font as tkfont
import customtkinter
import pandas as pd
import datetime
import pathlib
import os
import random
import threading



if not os.path.exists('log'):
    os.makedirs('log')
    print("created folder name log under this dir")

def validate_int(P):
    if P == '':
        return True
    if P.isdigit():
        P = int(P)
        return True
    else:
        return False

def setup_window():
    global new_window
    new_window = customtkinter.CTkToplevel(root)
    new_window.title("SET THIS BAD BOY UP")
    new_window.geometry("450x220")
    new_window.geometry("+720+345")
    new_window.columnconfigure(2, weight=1)
    new_window.columnconfigure(1, weight=1)


    #row 1 formatting label, empty, for format only
    format_label = customtkinter.CTkLabel(new_window, height = 50, width = 50, text="")
    format_label.grid(row=0, column=3)


    # register the logic of validation function
    validate = new_window.register(validate_int)



    #work time module
    # validate="key", validatecommand=(validation, "%P") to 
    desired_worktime = customtkinter.CTkLabel(new_window, height = 25, width = 50, text="Enter your desired work time: ")
    desired_worktime.grid(row=1, column=1)
    global worktime_input

    #call the logic of validation when key is pressed, validatecommand to callout the validation logic
    worktime_input = customtkinter.CTkEntry(master=new_window, placeholder_text=set_work_global, validate="key", validatecommand=(validate, "%P"))
    worktime_input.grid(row =1, column=2, sticky='ew')
    mintues_label = customtkinter.CTkLabel(new_window, text=" min(s) ")
    mintues_label.grid(row=1, column=3)

    #break time module
    breaktime = customtkinter.CTkLabel(new_window, width = 50, text="Enter your desired break time: ", )
    breaktime.grid(row=2, column=1)
    global breaktime_input

    #call the logic of validation when key is pressed, validatecommand to callout the validation logic
    breaktime_input = customtkinter.CTkEntry(master=new_window, placeholder_text=set_break_global, validate="key", validatecommand=(validate, "%P"))
    breaktime_input.grid(row=2, column=2, sticky='ew')

    mintues_label = customtkinter.CTkLabel(new_window, text=" min(s) ")
    mintues_label.grid(row=2, column=3)

    #Gap time module
    global gaptime_input
    gaptime = customtkinter.CTkLabel(new_window, width = 50, text="Buzz me randomly within: ", )
    gaptime.grid(row=3, column=1)
    gaptime_input = customtkinter.CTkEntry(master=new_window, placeholder_text=set_gap_global // 60, validate="key", validatecommand=(validate, "%P"))
    gaptime_input.grid(row=3, column=2, sticky='ew')
    mintues_label = customtkinter.CTkLabel(new_window, text=" min(s) ")
    mintues_label.grid(row=3, column=3)
    
    #format
    format_label = customtkinter.CTkLabel(new_window, height = 20, width = 20, text="")
    format_label.grid(row=4, column=0)

    #finish setup
    btn_setup_done = customtkinter.CTkButton(new_window, text='finish setting up', width=400, height=50, command=clock.setup_input)
    btn_setup_done.grid(row=5, column = 1, columnspan=2, sticky='ew')


save_count = 0
set_break_global = 5
set_work_global = 25
set_gap_global = 120
workstreak = pathlib.Path('log/workstreak.csv')
time_started = datetime.datetime.now().strftime('%H:%M:%S')
time_started_save = time_started
randombuzzcycle = True

class PomodoroClock:
    def __init__(self, master):
        self.master = master
        self.master.title("PmdC")
        self.work_time = set_work_global * 60 # 25 minutes
        self.break_time = set_break_global * 60  # 5 minutes
        self.current_time = self.work_time
        self.banked_break_time = 0
        self.running = False
        self.usingbank = False
        self.break_true = True
        self.timer = None
        self.work_streak = 0
        self.label = customtkinter.CTkLabel(self.master, text=self.time_to_string(self.current_time), font=("Helvetica", 40))
        self.label.pack(pady=5)

        self.label2 = customtkinter.CTkLabel(self.master, text=self.work_streak_statement(self.work_streak), font=("Helvetica", 10))
        self.label2.pack(pady=5)

        self.start_button = customtkinter.CTkButton(self.master, text="Start", command=self.start)
        self.start_button.pack(padx=5, pady=0)

        self.stop_button = customtkinter.CTkButton(self.master, text="Stop", command=self.stop)
        self.stop_button.pack(padx=5, pady=3)

        self.bank_button = customtkinter.CTkButton(self.master, text="Bank", command=self.bank)
        self.bank_button.pack(padx=5, pady=0)

        self.use_bank_button = customtkinter.CTkButton(self.master, text="Use up saved break", command=self.use_bank)
        self.use_bank_button.pack(padx=5, pady=3)
        self.setup_button = customtkinter.CTkButton(self.master, text='config', command=setup_window)
        self.setup_button.pack(padx=5, pady=0)
    def setup_input(self):
        try:
            if int(breaktime_input.get()) < 5:
                messagebox.showinfo('Value Error - Break Time','Break time too short! Please set it between 5 to 15 mins')
                return None
            elif int(breaktime_input.get()) > 15:
                messagebox.showinfo('Value Error - Break Time','Break time too long! Please set it between 5 to 15 mins')
                return None
            elif int(worktime_input.get()) < 5:
                messagebox.showinfo('Value Error - Work time','Work time too short! Please set it between 5 to 30 mins')
                return None
            elif int(worktime_input.get()) > 30:
                messagebox.showinfo('Value Error - Work time','Work time too long! Please set it between 5 to 30 mins')
                return None
            elif int(gaptime_input.get()) * 60 < int(worktime_input.get()) * 60:
                messagebox.showinfo('Value Error - Gap Time','Gap time too short! Please set it above 1 minute')
                return None
        except ValueError as e:
            return None
        global set_work_global
        try:
            set_work_global = int(worktime_input.get())
        except:
            pass
        global set_break_global
        try:
            set_break_global = int(breaktime_input.get())
        except:
            pass
        global set_gap_global
        set_gap_global = int(gaptime_input.get()) * 60
        print(f'changed gap time to {set_gap_global} secs')
        new_window.destroy()
        messagebox.showinfo('Success!', 'Work & Break time change will take effect after next break')

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
        if save_count == 1:
            working_streak_data = {
                'Recorded Day' : [datetime.date.today().strftime("%d/%m/%Y")],
                'Work streak of the session' : [work],
                'From' : [time_started_save],
                'Till' : [datetime.datetime.now().strftime('%H:%M:%S')]
            }
            df = pd.DataFrame(data=working_streak_data)
            df.to_csv("log/workstreak.csv", mode = 'a', header = not workstreak.exists(), index = False)
            
        elif workstreak.exists() and save_count > 1:
            opening_file = True
            while opening_file:
                try:
                    df = pd.read_csv('log/workstreak.csv', encoding='utf-8')
                    opening_file = False
                    break
                except:
                    messagebox.info('permission denied, try closing the workstreak.csv file then continue')
            if df.loc[df.index[-1], 'Recorded Day'] == datetime.date.today().strftime("%d/%m/%Y"):
                try:
                    df.loc[df.index[-1], 'Work streak of the session'] = work
                    df.loc[df.index[-1], 'Till'] = datetime.datetime.now().strftime('%H:%M:%S')
                    df.to_csv("log/workstreak.csv", mode = 'w', header = True, index = False)
                except:
                    print('Header not found')
        if save_count >= 1:
            writer = pd.ExcelWriter('log/workstreak.xlsx', engine='xlsxwriter')

        # Iterate over each CSV file
            opening_file = True
            while opening_file:
                try:
                    df = pd.read_csv('log/workstreak.csv')
                    opening_file = False
                    break
                except:
                    messagebox.info('permission denied, try closing the workstreak.csv file then continue')

            df.to_excel(writer, sheet_name='workstreak', index=False)
            saving_file = False

            # Access the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['workstreak']
                
            # Adjust the column widths
            for i, column in enumerate(df.columns):
                # Find the maximum length of a value in the column
                column_width = max(df[column].astype(str).map(len).max(), len(column))
                
                # Set the column width in the worksheet
                worksheet.set_column(i, i, column_width)


            # Save the Excel file

            writer._save()
                
        return f"Your current work streak: {work}"
    def randombuzzer(self, set_gap_global):
        global randombuzzcycle
        if self.running:
            randombuzzcycle = False
            # set_gap_global = 5 # delete hash for testing
            print(f'randombuzzer debug message::buzzer cycle is set to {randombuzzcycle} now')
            sleeping_time = random.randint(60, set_gap_global)
            print(f'randombuzzer debug message::sleeping time: {sleeping_time} secs')
            time.sleep(sleeping_time)
            waitsec = random.randint(10, 15)
            messagebox.showinfo('random buzzer', f"Take a break for {waitsec} secs! I will notify you when time\'s up")
            print(f'randombuzzer debug message::I will sleep for {waitsec} secs from now on')
            time.sleep(waitsec)
            messagebox.showinfo("Time\'s up!", 'Time to work!')
            randombuzzcycle = True
            print(f'randombuzzer debug message::buzzer cycle is set to {randombuzzcycle} now, I had slept for {waitsec} secs before you closed the messagebox window')

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
                    self.break_time = self.break_time
            if self.current_time == 0 and self.break_true == False:
                if self.usingbank == True:
                    self.usingbank = False
                elif self.usingbank == False:
                    self.work_streak += 1
                    global save_count 
                    save_count += 1
                    self.label2.configure(text=self.work_streak_statement(self.work_streak))
                self.break_true = True
                self.current_time = set_work_global * 60 #convert to min
                self.break_time = set_break_global * 60 #convert to min
                messagebox.showinfo('Time\'s up', 'Time for work!')
            if randombuzzcycle == True:
                threading.Thread(target=self.randombuzzer, group=None, args=(set_gap_global,)).start()
            self.timer = self.master.after(1000, self.update_clock)
        else:
            self.current_time = set_work_global

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.update_clock, group=None).start()
            

    def stop(self):
        if self.running:
            self.running = False
            if self.timer is not None:
                self.master.after_cancel(self.timer)
                self.timer = None



root = customtkinter.CTk()

# setup a test window




clock = PomodoroClock(root)


root.attributes('-topmost', 1)
root.geometry("210x270")
root.geometry("+400+300")

root.mainloop()

