import Tkinter
import ttk
import tkSimpleDialog
import tkMessageBox
import math
import tkColorChooser
import ImageTk

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

class BaseCanvasDraw(object):
    def __init__(self, canvas, coords, **kws):
        self.canvas = canvas
        self.coords = coords
        self.style = kws
        # override this to Canvas.create_something
        # self.draw_func = None
        self.__index = self.draw()

    def draw(self):
        return self.draw_func(*self.coords, **self.style)

    def update(self):
        self.canvas.coords(self.__index, *self.coords)
        self.canvas.itemconfig(self.__index, **self.style)

    def delete(self):
        self.canvas.delete(self.__index)

    def bind(self, *args, **kws):
        self.canvas.tag_bind(self.__index, *args, **kws)

class TextDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, text, **kws):
        self.draw_func = canvas.create_text
        BaseCanvasDraw.__init__(self, canvas, [x, y], text=text, **kws)

    @property
    def text(self):
        return self.style['text']

    @text.setter
    def text(self, value):
        self.style['text'] = str(value)

class ImageDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, image, **kws):
        '''
        image: can be string or ImageTk.PhotoImage instance
        '''
        self.draw_func = canvas.create_image
        BaseCanvasDraw.__init__(self, canvas,
            [x, y],
            image=ImageTk.PhotoImage(file=image) if type(image)==str else image, **kws)

    @property
    def image(self):
        return self.style['image']

    @image.setter
    def image(self, value):
        self.style['image'] = value
        self.update()

class RectangleDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, width, height, **kws):
        self.draw_func = canvas.create_rectangle
        BaseCanvasDraw.__init__(self, canvas, [x, y, x + width, y + height], **kws)

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, value):
        self.coords = [value, self.y, value+self.width, self.y+self.height]
        self.update()

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, value):
        self.coords = [self.x, value, self.x+self.width, value+self.height]
        self.update()

    @property
    def width(self):
        return self.coords[2] - self.coords[0]

    @width.setter
    def width(self, value):
        self.coords = [self.x, self.y, self.x+value, self.y+self.height]
        self.update()

    @property
    def height(self):
        return self.coords[3] - self.coords[1]

    @height.setter
    def height(self, value):
        self.coords = [self.x, self.y, self.x+self.width, self.y + value]
        self.update()

class OvalDraw(RectangleDraw):
    def __init__(self, canvas, x, y, width, height, **kws):
        self.draw_func = canvas.create_oval
        RectangleDraw.__init__(self, canvas, x, y, width, height, **kws)

    @property
    def radius(self):
        if self.width == self.height:
            return self.width
        raise Exception('Oval is not a circle')

    @radius.setter
    def radius(self, value):
        self.width = value
        self.height = value

    # TODO: implements to set the center
    @property
    def center_x(self):
        raise NotImplementedError

class PolygonDraw(BaseCanvasDraw):
    def __init__(self, canvas, coords, **kws):
        self.draw_func = canvas.create_polygon
        BaseCanvasDraw.__init__(self, canvas, coords, **kws)

# TODO
class RoundedRectangleDraw(PolygonDraw):
    def __init__(self, *args, **kws):
        raise NotImplementedError

class ExtendedCanvas(Tkinter.Canvas):
    def __init__(self, *args, **kwargs):
        Tkinter.Canvas.__init__(self, *args, **kwargs)

    @property
    def width(self):
        return int(self['width']) - 1

    @property
    def height(self):
        return int(self['height']) - 1

    def get_circle_point(self, cx, cy, radius, angle):
        '''
        Returns the position of a vertex2D of a circle
        which center is in [cx,cy] position and radius 'radius'
        in the angle 'angle'
        '''
        # angle in degree
        angle = math.radians(angle)
        y = math.sin(angle) * radius
        x = math.cos(angle) * radius
        x += cx
        y = cy - y
        return [x, y]

    def create_rounded_rectangle(self, pos, radius, **kwargs):
        '''
        pos: [x1, y1, x2, y2]
        radius: [nw, sw, se, ne]
        '''
        pts = []
        # NW
        if radius[0]:
            cx = pos[0] + radius[0]
            cy = pos[1] + radius[0]
            for i in range(90, 180):
                pts.extend(self.get_circle_point(cx,cy,
                    radius[0], i))
        else:
            pts.extend([pos[0], pos[1]])
        # SW
        if radius[1]:
            cx = pos[0] + radius[1]
            cy = pos[3] - radius[1]
            for i in range(180, 270):
                pts.extend(self.get_circle_point(cx, cy,
                    radius[1], i))
        else:
            pts.extend([pos[0], pos[3]])

        # SE
        if radius[2]:
            cx = pos[2] - radius[2]
            cy = pos[3] - radius[2]
            for i in range(270, 360):
                pts.extend(self.get_circle_point(cx,cy,
                    radius[2],i))
        else:
            pts.extend([pos[2],
                pos[3]])
        # NE
        if radius[3]:
            cx = pos[2] - radius[3]
            cy = pos[1] + radius[3]
            for i in range(0, 90):
                pts.extend(self.get_circle_point(cx,cy,
                    radius[3],i))
        else:
            pts.extend([pos[2],
                pos[1]])
        return self.create_polygon(*pts, **kwargs)

class ExtendedListboxItem(object):
    '''
    before_click: function called before the click selection
    '''
    def __init__(self, canvas, title, subtitle, icon, height, yoffset, before_click):
        self.canvas = canvas
        self.__before_click = before_click
        self.__selected = False
        self.__rec_bg = RectangleDraw(canvas, 1, 1+yoffset,
            canvas.width, 40, fill=self.canvas['bg'], outline='')

        self.__title = TextDraw(canvas, 50, 10 + yoffset, title,
            anchor='nw', font=('TkDefaultFont',10))
        self.__subtitle = TextDraw(canvas, 50, 25 + yoffset,
            subtitle, anchor='nw', font=('TkDefaultFont',8), fill='#555')
        self.__icon = ImageDraw(self.canvas, 5, 6+yoffset, icon, anchor='nw') if icon else None

        self.bind('<Enter>', self.__mouse_over, '+')
        self.bind('<Leave>', self.__mouse_leave, '+')
        self.bind('<1>', self.__on_click, '+')

    def __on_click(self, evt):
        if self.__before_click:
            self.__before_click()
        self.selected = True

    def bind(self, *args, **kws):
        self.__rec_bg.bind(*args, **kws)
        self.__title.bind(*args, **kws)
        self.__subtitle.bind(*args, **kws)
        if self.__icon:
            self.__icon.bind(*args, **kws)

    def __mouse_over(self, evt):
        self.__rec_bg.style['fill'] = '#bbb'
        self.__rec_bg.update()

    def __mouse_leave(self, evt):
        if self.__selected:
            self.__rec_bg.style['fill'] = '#00bbdd'
        else:
            self.__rec_bg.style['fill'] = self.canvas['bg']
        self.__rec_bg.update()

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value):
        self.__selected = bool(value)
        self.__mouse_leave(None)

    def delete(self):
        self.__rec_bg.delete()
        self.__title.delete()
        self.__subtitle.delete()
        if self.__icon:
            self.__icon.delete()

    @property
    def title(self):
        return self.__title.text

    @title.setter
    def title(self, value):
        self.__title.text = value

    @property
    def subtitle(self):
        return self.__subtitle.text

    @subtitle.setter
    def subtitle(self, value):
        self.__subtitle.text = value

    @property
    def icon(self):
        return self.__icon.image

    # is not possible set icon because
    # any bind already made cant be applyed
    # to image
    # @icon.setter
    # def icon(self, value):
    #     self.__icon.image = value

class ExtendedListbox(ExtendedCanvas):
    '''
    '''
    def __init__(self, *args, **kws):
        self.__items = []
        self.item_height = kws.pop('item_height', 40)
        ExtendedCanvas.__init__(self, *args, **kws)

    def add_item(self, title, subtitle=None, icon=None):
        item = ExtendedListboxItem(self, title, subtitle, icon,
            self.item_height, self.item_height * len(self.__items),
            self.desselect_all)
        self.__items.append(item)

    def remove_by_title(self, title):
        for i in self.__items:
            if i.title == title:
                i.delete()
                self.__items.remove(i)
        self.redraw()

    def remove_by_index(self, index):
        self.__items.pop(index).delete()
        self.redraw()

    def get_selected(self):
        '''
        returns the item selected
        '''
        for i in self.__items:
            if i.selected:
                return i
        return None

    def select_last(self):
        if len(self.__items) > 0:
            self.__items[-1].selected = True

    def select_first(self):
        if len(self.__items) > 0:
            self.__items[0].selected = True

    def desselect_all(self):
        for i in self.__items:
            i.selected = False

    def delete_all(self):
        for i in self.__items:
            i.delete()
        self.__items = []
        self.redraw()

    def redraw(self):
        _old_list = self.__items
        self.__items = []
        for i in _old_list:
            i.delete()
            item = ExtendedListboxItem(self, i.title, i.subtitle, i.icon,
                self.item_height, self.item_height * len(self.__items),
                self.desselect_all)
            self.__items.append(item)

class ColorChooser(ExtendedCanvas, object):
    '''
    To get/set the color use 'color' property
    '''
    def __init__(self, parent, initial_color, **kws):
        kws.update(bg=parent['bg'], bd=0, highlightthickness=0)
        ExtendedCanvas.__init__(self, parent, **kws)
        self.__color_index = self.__gen_index(initial_color)
        self.__color = initial_color
        self.bind('<1>', self.__show_chooser, '+')

    def __show_chooser(self, evt):
        rgb = tkColorChooser.askcolor(color=self.__color)[1]
        if rgb:
            self.color = rgb

    def __gen_index(self, initial_color):
        return self.create_rounded_rectangle([0, 0, self.width, self.height],
            [5,5,5,5], fill=initial_color, outline=initial_color)

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value
        self.update()

    def update(self):
        ExtendedCanvas.update(self)
        self.delete(self.__color_index)
        self.__color_index = self.__gen_index(self.color)

class Frame(Tkinter.Frame):
    def __init__(self, *args, **kwargs):
        Tkinter.Frame.__init__(self, *args, **kwargs)
        self['bg'] = self.master['bg']

class Button(ExtendedCanvas):
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

    def __create_bg_index(self):
        return self.create_rounded_rectangle([0,0,self.width,self.height],
            self.radius, fill=self.__bg_color, outline=self.__bd_color)

    def __create_text_index(self):
        return self.create_text(self.width / 2,
            self.height / 2,
            fill=self.__fg_color,
            text=self.text)

    def __bind_command(self, cmd):
        if not cmd:
            return
        self.bind('<1>', lambda *args : cmd(), '+')

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

class Entry(ttk.Entry, object):
    def __init__(self, *args, **kws):
        ttk.Entry.__init__(self, *args, **kws)

    @property
    def text(self):
        return self.get()

    @text.setter
    def text(self, value):
        self.delete(0, 'end')
        self.insert(0, str(value))

class Listbox(Tkinter.Listbox):
    def __init__(self, *args, **kwargs):
        Tkinter.Listbox.__init__(self, *args, **kwargs)
        self['bg'] = '#d1d8e0'
        self['relief'] = 'flat'
        self['highlightthickness'] = 0
        self['selectbackground'] = '#c7ccd1'
        self['activestyle'] = 'none'

class OptionMenu(Tkinter.OptionMenu):
    pass

class MessageBox:
    @staticmethod
    def warning(**kws):
        tkMessageBox.showwarning(**kws)

class DefaultDialog(Tkinter.Toplevel):
    '''
    Class to open dialogs.
    This class is intended as a base class for custom dialogs
    '''
    def __init__(self, parent, title=None):
        '''
        Initialize a dialog.
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
        self.resizable(0, 0)
        self.deiconify()  # become visibile now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self):
        self.initial_focus = None
        Tkinter.Toplevel.destroy(self)

    def body(self, master):
        '''
        create dialog body.
        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        pass

    def buttonbox(self):
        '''
        add standard button box.
        override if you do not want the standard buttons
        '''
        box = Frame(self)

        w = Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        w = Button(box, text="Cancel", command=self.cancel)
        w.pack(side='left', padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side='right')

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
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

    def validate(self):
        '''
        validate the data
        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        '''
        return 1  # override

    def apply(self):
        '''
        process the data
        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        '''
        pass  # override

class OkCancel(DefaultDialog):
    def __init__(self, parent, msg, title=None):
        self.msg = msg
        DefaultDialog.__init__(self, parent, title)

    def body(self, parent):
        self.output = False
        l = Label(parent, text=self.msg)
        l.pack()
        return l

    def apply(self):
        self.output = True

from newproject import NewProjectWindow
from about import AboutWindow
from assetsmanager import AssetsManagerWindow
from settings import SettingsWindow
from scene import AddSceneWindow