from Tkinter import Toplevel
import ttk
from . import *

class AboutWindow:
    def __init__(self, master):
        self._toplevel = Toplevel()
        ttk.Label(self._toplevel, text='Phaser Editor').grid(pady=45, padx=45)

        center(self._toplevel)
        self._toplevel.focus_force()
        self._toplevel.bind('<Escape>', lambda *args: self._toplevel.destroy(), '+')