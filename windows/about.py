from Tkinter import *
from . import *
import tkSimpleDialog

class AboutWindow(tkSimpleDialog.Dialog ):
    def body(self, master):
        Label(master, text='Phaser Editor').grid(pady=45, padx=45)
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        box.pack()