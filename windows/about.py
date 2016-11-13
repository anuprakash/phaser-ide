from . import *

class AboutWindow(DefaultDialog):
    def body(self, master):
        return Label(master, text='Phaser Editor').grid(pady=45, padx=45)
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        box.pack()
