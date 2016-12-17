# coding: utf-8

import boring.dialog
import boring.widgets

LABEL = '''
## Shortcuts

*Control+N*    Creates a new project
*Control+M*    Creates a new scene
*Control+X*    Creates a new sprite
*Control+S*    Saves the current project as a JSON file
*Control+O*    Opens a JSON project file
*Alt+P*        Shows the project properties
'''

class ShortcutsWindow(boring.dialog.DefaultDialog):
    def body(self, master):
        mdl = boring.widgets.MarkDownLabel(
            master,
            height=20,
            text=LABEL
        )
        mdl.grid(
            pady=45, padx=45
        )
        return mdl
    
    def buttonbox(self):
        box = boring.widgets.Frame(self)
        w = boring.widgets.Button(
            box,
            text='OK',
            command=self.ok,
            default='active'
        )
        w.pack(side='left', padx=5, pady=5)
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.ok)
        box.pack()
        return w