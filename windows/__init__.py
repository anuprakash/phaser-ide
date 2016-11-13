from Tkinter import Toplevel
import Tkinter
import ttk
import tkSimpleDialog
import tkMessageBox

def center(widget):
    widget.update_idletasks()
    sw = int(widget.winfo_screenwidth())
    sh = int(widget.winfo_screenheight())
    ww = int(widget.winfo_width())
    wh = int(widget.winfo_height())
    xpos = (sw / 2) - (ww / 2)
    ypos = (sh / 2) - (wh / 2)
    widget.geometry('%dx%d+%d+%d' % (ww, wh, xpos, ypos))

class Frame(Tkinter.Frame):
    pass

class Button(ttk.Button):
    pass

class DefaultDialog(tkSimpleDialog.Dialog):
    pass

class Label(Tkinter.Label):
    pass

class Entry(ttk.Entry):
    pass

class Listbox(Tkinter.Listbox):
    pass

class OptionMenu(Tkinter.OptionMenu):
    pass

class MessageBox:
    @staticmethod
    def warning(**kws):
        tkMessageBox.showwarning(**kws)

from newproject import NewProjectWindow
from about import AboutWindow
from assetsmanager import AssetsManagerWindow
from settings import SettingsWindow