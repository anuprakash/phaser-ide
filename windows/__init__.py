import Tkinter
import ttk
import tkSimpleDialog
import tkMessageBox
import math

BG_COLOR = '#ededed'

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
    def __init__(self, *args, **kwargs):
        Tkinter.Frame.__init__(self, *args, **kwargs)
        self['bg'] = self.master['bg']

class Button(Tkinter.Canvas):
    def __init__(self, *args, **kwargs):
        _wi, _he = kwargs.pop('width', 100), kwargs.pop('height', 25)
        self.radius = [4, 4, 4, 4]
        self.level = 1
        self.__bd_color = '#c7c7c7'
        self.__bg_color = '#ffffff'
        self.__fg_color = 'black'

        self.default = kwargs.pop('default', '')
        self.text = kwargs.pop('text', '')
        self.command = kwargs.pop('command', None)

        if self.default == 'active':
            self.__bg_color = '#0088ff'
            self.__fg_color = 'white'
            self.__bd_color = None

        kwargs.update(width=_wi, height=_he, bg=BG_COLOR)
        Tkinter.Canvas.__init__(self, *args, **kwargs)
        self.update_idletasks()
        self.__bg_index = self.__create_bg_index()
        self.__text_index = self.__create_text_index()

        self.__bind_command(self.command)

        self.config(bg=self.master['bg'],
            relief='flat', bd=0,
            highlightthickness=0)

    @property
    def width(self):
        return int(self['width']) - 1

    @property
    def height(self):
        return int(self['height']) - 1

    def __create_bg_index(self):
        return self.create_polygon(*self.get_coords(),
            fill=self.__bg_color,
            outline=self.__bd_color)

    def __create_text_index(self):
        return self.create_text(self.width / 2,
            self.height / 2,
            fill=self.__fg_color,
            text=self.text)

    def __bind_command(self, cmd):
        if not cmd:
            return
        self.bind('<1>', lambda *args : cmd(), '+')

    def get_circle_point(self, cx,cy,radius,angle):
        """
        Returns the position of a vertex2D of a circle
        which center is in [cx,cy] position and radius 'radius'
        in the angle 'angle'
        """
        # angle in degree
        angle = math.radians(angle)
        y = math.sin(angle) * radius
        x = math.cos(angle) * radius
        x += cx
        y = cy - y
        return [x,y]

    def get_coords(self):
        pts = []
        # NW
        if self.radius[0]:
            cx = self.radius[0]
            cy = self.radius[0]
            for i in range(90,180,self.level):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[0], i))
        else:
            pts.extend([0, 0])
        # SW
        if self.radius[1]:
            cx = self.radius[1]
            cy = self.height - self.radius[1]
            for i in range(180,270,self.level):
                pts.extend(self.get_circle_point(cx, cy,
                    self.radius[1], i))
        else:
            pts.extend([0, self.height])

        # SE
        if self.radius[2]:
            cx = self.width-self.radius[2]
            cy = self.height-self.radius[2]
            for i in range(270,360,self.level):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[2],i))
        else:
            pts.extend([self.width,
                self.height])
        # NE
        if self.radius[3]:
            cx = self.width-self.radius[3]
            cy = self.radius[3]
            for i in range(0,90,self.level):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[3],i))
        else:
            pts.extend([self.width,
                0])
        return pts

class Label(Tkinter.Label):
    def __init__(self, *args, **kwargs):
        Tkinter.Label.__init__(self, *args, **kwargs)
        self['bg'] = self.master['bg']

    def pack(self, *args, **kwargs):
        x, y = kwargs.pop('padx', 5), kwargs.pop('pady', 5)
        kwargs.update(padx=x, pady=y)
        Tkinter.Label.pack(self, *args, **kwargs)

    def grid(self, *args, **kwargs):
        x, y = kwargs.pop('padx', 5), kwargs.pop('pady', 5)
        kwargs.update(padx=x, pady=y)
        Tkinter.Label.grid(self, *args, **kwargs)

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
        self['bg'] = parent['bg']

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

        center(self)
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

        w = Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        w = Button(box, text="Cancel", command=self.cancel)
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
from scene import AddSceneWindow