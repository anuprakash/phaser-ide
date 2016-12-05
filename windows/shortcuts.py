# coding: utf-8

from . import *

LABEL = '''
## Shortcuts

*Control+N*    Creates a new project
*Control+M*    Creates a new scene
*Control+X*    Creates a new sprite
*Control+S*    Saves the current project as a JSON file
*Control+O*    Opens a JSON project file
*Alt+P*        Shows the project properties
'''

class ShortcutsWindow(DefaultDialog):
    def body(self, master):
        mdl = MarkDownLabel(master, height=20, text=LABEL)
        mdl.grid(pady=45, padx=45)
        return mdl
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        box.pack()