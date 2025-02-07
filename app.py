from sre_parse import State
from tkinter import *

import time
import threading
from threading import Timer
import numpy as np
from queue import PriorityQueue

from matplotlib.pyplot import text

C_ORANGE = "#D6A171"
C_GREEN = "#D8D6A3"
C_WHITE = "#E5E5E5"
C_BLACK = "#000000"
TEXT_COLOUR = "#EAECEE"


FONT = "Helvetica 14"
BOLD_FONT = "Helvetica 14 bold"

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Application:

    def __init__(self):
        self.type = "General"
        self.window = Tk()
        self._setup_main_window()
        self.order_number = 100
        self.orders = []
        self.processing = []
        self.complete_list = []
        self.bot = 0
        self.counter = 0
        self.counter2 = 0
        self.threadLock = threading.Lock()

    def _setup_main_window(self):
        self.window.title("MCD")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=650, height=550, bg=C_WHITE)

        #head label
        head_label = Label(self.window, bg=C_WHITE, fg=C_BLACK, text='Automated Cooking Bots',font=BOLD_FONT, pady=10)
        head_label.place(relwidth=1)

        #divider
        line = Label(self.window, width=450, bg=C_WHITE)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        #head label
        process_label = Label(self.window, bg=C_ORANGE, fg=C_BLACK, text='Pending',font=FONT, pady=10)
        process_label.place(relwidth=0.5, relx=0, rely= 0.08)

        #head label
        complete_label = Label(self.window, bg=C_GREEN, fg=C_BLACK, text='Completed',font=FONT, pady=10)
        complete_label.place(relwidth=0.5, relx=0.5, rely= 0.08)

        #text widget
        self.pending = Text(self.window, width=20, height=2, bg=C_GREEN, fg=C_BLACK, font=FONT, padx=5, pady=5)
        self.pending.place(relheight=0.6, relwidth=0.5, relx=0.001, rely= 0.16)
        self.pending.configure(cursor='arrow', state=DISABLED)

        #scroll bar
        scrollbar = Scrollbar(self.pending)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.pending.yview)

        #text widget
        self.complete = Text(self.window, width=20, height=2, bg=C_GREEN, fg=C_BLACK, font=FONT, padx=5, pady=5)
        self.complete.place(relheight=0.6, relwidth=0.5, relx=0.5, rely= 0.16)
        self.complete.configure(cursor='arrow', state=DISABLED)

        #scroll bar
        scrollbar = Scrollbar(self.complete)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.pending.yview)
        
        #bottom label
        bottom_label = Label(self.window, bg=C_WHITE,height=50)
        bottom_label.place(relwidth=1, rely=0.76)

        #normal order button
        normal_btn = Button(bottom_label, text="Normal Order", font=FONT, width=20, bg=C_ORANGE, command=lambda:self._new_order())
        normal_btn.place(relx=0.1, rely=0.022, relheight=0.04, relwidth=0.25)

        #vip order button
        vip_btn = Button(bottom_label, text="VIP Order", font=FONT, width=20, bg=C_ORANGE, command=lambda:self._new_vip_order())
        vip_btn.place(relx=0.1, rely=0.082, relheight=0.04, relwidth=0.25)

        #no of bots text widget
        self.settings = Text(bottom_label, width=4, height=2, bg=C_GREEN, fg=C_BLACK, font=FONT, pady = 10)
        self.settings.place(relx=0.63, rely=0.03, relheight=0.05, relwidth=0.3)
        self.settings.configure(cursor='arrow', state=DISABLED)

        #plus bot button
        plus_btn = Button(bottom_label, text="+", font=FONT, width=20, bg=C_ORANGE, command=lambda:self._add_bot())
        plus_btn.place(relx=0.65, rely=0.09, relheight=0.03, relwidth=0.1)

        #minus bot button
        minus_btn = Button(bottom_label, text="-", font=FONT, width=20, bg=C_ORANGE, command=lambda:self._minus_bot())
        minus_btn.place(relx=0.8, rely=0.09, relheight=0.03, relwidth=0.1)

    def waitForThis(self):
        done_msg = f"Order {self.processing[self.counter2][1]} Completed \n\n"
        self.counter2 = self.counter2 + 1
        self.complete.configure(state=NORMAL)
        self.complete.insert('1.0', done_msg)
        self.complete.configure(state=DISABLED)
        # after threading timer, 'waitForThis' gets executed
        self.pending.configure(state=NORMAL)
        self.pending.delete('1.0', END)
        self.pending.configure(state=DISABLED)

    #timer for ordering
    def _new_order(self):
        self.orders.append((2, self.order_number))
        self.counter = self.counter + 1
        self.processing = sorted(self.orders, key=lambda x: x[0], reverse=True)
        self.order_number = self.order_number + 1
        


    def _new_vip_order(self):
        self.orders.append((1, self.order_number))
        self.counter = self.counter + 1
        self.order_number = self.order_number + 1
        self.processing = sorted(self.orders, key=lambda x: x[0], reverse=True)
        
    def _add_bot(self):
        self.bot = self.bot + 1
        bot_msg = f"Number of Bots: {self.bot}\n\n"
        self.settings.configure(state=NORMAL)
        self.settings.insert('1.0', bot_msg)
        self.settings.configure(state=DISABLED)
            
    def _minus_bot(self):
        self.bot = np.maximum(0, self.bot - 1)
        bot_msg = f"Number of Bots: {self.bot}\n\n"
        self.settings.configure(state=NORMAL)
        self.settings.insert('1.0', bot_msg)
        self.settings.configure(state=DISABLED)
    

    def run_gui(self):
        print('refresh')
        self.window.after(1000, self.refresh)
        self.window.mainloop()

    def refresh(self):
        print('refresh')
        
        # after threading timer, 'waitForThis' gets executed

        if self.bot > 0:
            if len(self.processing) > 0:
                order = self.processing.pop()
                self.complete_list.append(order)

        self.complete.configure(state=NORMAL)
        self.complete.delete('1.0', END)

        for order in self.complete_list:
            msg = f"Food Order {order} Completed \n\n"
            self.complete.insert('1.0', msg)

        self.pending.configure(state=NORMAL)
        self.pending.delete('1.0', END)
            
        for order in self.processing:
             msg = f"Food Order {order} Processing \n\n"
             self.pending.insert('1.0', msg)


        self.complete.configure(state=DISABLED)
        self.pending.configure(state=DISABLED)
        self.window.after(1000, self.refresh)

if __name__ == '__main__':
    gui = Application()
    gui.run_gui()