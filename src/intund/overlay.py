import sys

from tkinter import *
from tkinter.ttk import *

from . import controller


class Overlay:
    def __init__(self, bot):
        self.bot = bot

        self.root = Tk()
        self.root.wm_title('Intuitive Understanding')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', '0.6')
        self.root.configure(background='black')
        self.root.overrideredirect(True)
        self.root.geometry('600x290+1320+0')

        self.text = Text(self.root, font=('Lucida Console', 64), wrap=WORD,
                         highlightthickness=0, padx=4, pady=4, relief='flat')
        self.text.configure(background='black')
        self.text.configure(foreground='white')
        self.text.pack()

    def set_text(self, msg):
        self.text.delete('1.0', END)
        self.text.insert(END, msg)

    def update(self):
        if self.bot.ready:
            text = 'X: {:07.3f}, Y: {:07.3f}, Z: {:07.3f}'
            text = text.format(*self.bot.get_position())
            self.set_text(text)
        self.root.after(50, self.update)

    def run(self):
        self.root.after(50, self.update)
        self.root.mainloop()
