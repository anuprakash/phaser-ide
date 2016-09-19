import Tkinter
import tkSimpleDialog
import tkMessageBox
from . import default_attrs, default_pad

class NewProjectWindow(tkSimpleDialog.Dialog):
    def __init__(self, master, phaserproject, do_on_end=None):
        self.phaserproject = phaserproject
        self.do_on_end = do_on_end
        tkSimpleDialog.Dialog.__init__(self, master, title="New project")
    
    def body(self, master):
        Tkinter.Label(master, text="Project name", **default_attrs).grid(sticky='W', row=0, column=0, columnspan=4, **default_pad)
        self.name_entry = Tkinter.Entry(master, width=45)
        self.name_entry.grid(row=1, column=0, columnspan=4, **default_pad)
        self.name_entry.focus_force()
        self.name_entry.insert(0, self.phaserproject.name)

        Tkinter.Label(master, text='Width: ', **default_attrs).grid(row=2, column=0, sticky='W', **default_pad)

        self.width = Tkinter.Entry(master, width=4)
        self.width.grid(row=2, column=1, sticky='W', **default_pad)
        self.width.insert(0, str(self.phaserproject.width))

        Tkinter.Label(master, text='Height: ', **default_attrs).grid(row=2, column=2, sticky='W', **default_pad)

        self.height = Tkinter.Entry(master, width=4)
        self.height.grid(row=2, column=3, sticky='W', **default_pad)
        self.height.insert(0, str(self.phaserproject.height))

        # Tkinter.Button(master, text="ok", command=self.__ok_callback).grid(row=3, column=2, **default_pad)
        # Tkinter.Button(master, text="cancel", command=self.__cancel_callback).grid(row=3, column=3, **default_pad)

        return self.name_entry
    
    def apply(self):
        '''
        called when ok button is pressed
        '''
        width, height = 0, 0
        try:
            width = int(self.width.get())
            height = int(self.height.get())
        except:
            print 'Invalid width or height'

        self.phaserproject.width = width
        self.phaserproject.height = height
        self.phaserproject.name = self.name_entry.get()

        if self.do_on_end:
            self.do_on_end(self.phaserproject)
    
    def validate(self):
        width, height = 0, 0
        try:
            width = int(self.width.get())
            height = int(self.height.get())
        except:
            tkMessageBox.showwarning(title='Wrong data', message='Invalid width/height')
            return False
        if not self.name_entry.get():
            tkMessageBox.showwarning(title='Project title', message='Invalid project name')
            return False
        return True