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

class DefaultDialog(Tkinter.Toplevel):
    '''Class to open dialogs.
    This class is intended as a base class for custom dialogs
    '''
    def __init__(self, parent, title=None):
        '''Initialize a dialog.
        Arguments:
            parent -- a parent window (the application window)
            title -- the dialog title
        '''
        Tkinter.Toplevel.__init__(self, parent)

        self.withdraw()
        # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                      parent.winfo_rooty() + 50))

        self.deiconify()  # become visibile now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self):
        '''Destroy the window'''
        self.initial_focus = None
        Tkinter.Toplevel.destroy(self)

    #
    # construction hooks

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        pass

    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side='left', padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        '''validate the data

        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        '''
        return 1  # override

    def apply(self):
        '''process the data

        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        '''
        pass  # override

from newproject import NewProjectWindow
from about import AboutWindow
from assetsmanager import AssetsManagerWindow
from settings import SettingsWindow