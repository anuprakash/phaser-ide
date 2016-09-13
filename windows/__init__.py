from Tkinter import Toplevel
default_pad = {
    'padx': 5,
    'pady': 5
}

default_attrs = {
    'background': 'white'
}

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        cls._instances[cls].focus()
        return cls._instances[cls]

def center(widget):
    widget.update_idletasks()
    sw = int(widget.winfo_screenwidth())
    sh = int(widget.winfo_screenheight())
    ww = int(widget.winfo_width())
    wh = int(widget.winfo_height())
    xpos = (sw / 2) - (ww / 2)
    ypos = (sh / 2) - (wh / 2)
    widget.geometry('%dx%d+%d+%d' % (ww, wh, xpos, ypos))

class DefaultWindow:
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
        self._toplevel.bind('<Escape>', lambda *args : self._toplevel.withdraw(), '+')
        self._toplevel.state('normal')
        self._toplevel.focus_force()
    
    def focus(self):
        '''
        needed for Singleton meta class
        '''
        self._toplevel.state('normal')
        self._toplevel.focus_force()
    
    def centralize(self):
        self._toplevel.update_idletasks()
        center(self._toplevel)

from newproject import NewProjectWindow
from about import AboutWindow
from assetsmanager import AssetsManagerWindow