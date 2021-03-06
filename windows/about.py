# coding: utf-8

import boring.dialog
import boring.widgets

ABOUT_LABEL = '''
## Author
### Willie Lawrence - http://vls2.tk
*Icons*: https://www.iconfinder.com/iconsets/small-n-flat
'''

class AboutWindow(boring.dialog.DefaultDialog):
    def body(self, master):
        mdl = boring.widgets.MarkDownLabel(
            master,
            height=20,
            text=ABOUT_LABEL
        )
        mdl.grid(
            pady=45,
            padx=45
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
        w.pack(
            side='left',
            padx=5,
            pady=5
        )
        self.bind(
            '<Return>',
            self.ok
        )
        self.bind(
            '<Escape>',
            self.ok
        )
        box.pack()