from Tkinter import Toplevel
import ttk
from . import *

class NewProjectWindow:
    __metaclass__ = Singleton
    '''
    args:
        + master: a Tk instance
        + phaserproject: a core.PhaserProject object to be editted
        + do_on_end: a function that is runned on end, it receives a project as argument
    '''
    def __init__(self, master, phaserproject, do_on_end=None):
        self.phaserproject = phaserproject
        self.do_on_end = do_on_end
        self._toplevel = Toplevel(master)
        self._toplevel.resizable(0, 0)
        ttk.Label(self._toplevel, text="Project name").grid(sticky='W', row=0, column=0, columnspan=4, **default_pad)
        self.name_entry = ttk.Entry(self._toplevel, width=45)
        self.name_entry.grid(row=1, column=0, columnspan=4, **default_pad)
        self.name_entry.focus_force()
        self.name_entry.insert(0, phaserproject.name)

        ttk.Label(self._toplevel, text='Width: ').grid(row=2, column=0, sticky='W', **default_pad)

        self.width = ttk.Entry(self._toplevel, width=4)
        self.width.grid(row=2, column=1, sticky='W', **default_pad)
        self.width.insert(0, str(phaserproject.width))

        ttk.Label(self._toplevel, text='Height: ').grid(row=2, column=2, sticky='W', **default_pad)

        self.height = ttk.Entry(self._toplevel, width=4)
        self.height.grid(row=2, column=3, sticky='W', **default_pad)
        self.height.insert(0, str(phaserproject.height))

        ttk.Button(self._toplevel, text="ok", command=self.__ok_callback).grid(row=3, column=2, **default_pad)
        ttk.Button(self._toplevel, text="cancel", command=self.__cancel_callback).grid(row=3, column=3, **default_pad)

        center(self._toplevel)
        self._toplevel.bind('<Escape>', lambda *args : self._toplevel.withdraw(), '+')
    
    def __ok_callback(self):
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

        self._toplevel.withdraw()
        if self.do_on_end:
            self.do_on_end(self.phaserproject)
    
    def __cancel_callback(self):
        '''
        called when cancel button is pressed
        '''
        self._toplevel.withdraw()

    def focus(self):
        '''
        needed for Singleton meta class
        '''
        self._toplevel.state('normal')
        self._toplevel.focus_force()