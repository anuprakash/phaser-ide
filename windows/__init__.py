import Tkinter
import ttk
import tkSimpleDialog
import math
import tkColorChooser
import ImageTk
import tkFont
import random
import string

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

    def up(self):
        self.canvas.tag_raise(self.__index)

    def down(self):
        self.canvas.tag_lower(self.__index)

    def reset(self):
        '''
        redraws and change the index
        '''
        self.delete()
        self.__index = self.draw()

class TextDraw(BaseCanvasDraw):
    def __init__(self, canvas, x, y, text, **kws):
        self.draw_func = canvas.create_text
        BaseCanvasDraw.__init__(self, canvas, [x, y], text=text, **kws)

    @property
    def text(self):
        return self.style['text']

    @text.setter
    def text(self, value):
        self.style['text'] = unicode(value)
        self.update()

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

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, value):
        self.coords = [value, self.y]
        self.update()

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, value):
        self.coords = [self.x, value]
        self.update()

    @property
    def width(self):
        return self.style.get('image').width()

    @width.setter
    def width(self, value):
        self.update() # TOdO

    @property
    def height(self):
        return self.style.get('image').height()

    @height.setter
    def height(self, value):
        self.update() # TODo

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
        self.coords = [self.x, self.y, self.x + self.width, self.y + value]
        self.update()

class OvalDraw(RectangleDraw):
    def __init__(self, canvas, x, y, width, height, **kws):
        RectangleDraw.__init__(self, canvas, x, y, width, height, **kws)
        self.draw_func = canvas.create_oval
        self.reset()

    @property
    def radius(self):
        if self.width == self.height:
            return self.width / 2
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

def draggable(item, update=None, init=None, end=None):
    '''
    item: must have x and y attributes and bind method
    update(event): function called at each mouse movement
    init(event): function called in the first click
    end(event): function called in release of mouse

    use item.draggable to set if item is draggable or not
    '''
    item.mouse_offset = None
    item.draggable = True
    def __click(evt):
        if not item.draggable:
            return
        item.mouse_offset = [evt.x - item.x, evt.y - item.y]
        if init:
            init(evt)
    item.bind('<1>', __click, '+')
    def __release(evt):
        if not item.draggable:
            return
        item.mouse_offset = None
        if end:
            end(evt)
    item.bind('<ButtonRelease-1>', __release, '+')
    def __drag(evt):
        if not item.draggable:
            return
        item.x = evt.x - item.mouse_offset[0]
        item.y = evt.y - item.mouse_offset[1]
        if update:
            update(evt)
    item.bind('<B1-Motion>', __drag, '+')

DRAG_CONTROL_STYLE = {
    'fill': '#00aacc',
    'outline': '#333'
}
def change_control_point_color(item):
    '''
    when mouse is over a control point
    the control points changes your color
    '''
    def __over(event):
        item.style['outline'] = 'red'
        item.update()
    item.bind('<Enter>', __over, '+')
    def __leave(event):
        item.style = DRAG_CONTROL_STYLE
        item.update()
    item.bind('<Leave>', __leave, '+')

def update_control_points(item):
    item.lower_right.x = item.x+item.width-item.lower_right.radius
    item.lower_right.y = item.y+item.height-item.lower_right.radius

    item.bounds.x = item.x
    item.bounds.y = item.y
    item.bounds.width = item.image.width()
    item.bounds.height = item.image.height()
    # put control points over every thing inside canvas
    item.lower_right.up()

def drag_control(item, radius=5):
    '''
    create dragcontrol points
    radius: the radius of each control point

    item: must have x, y, width and height attributes and bind method
    '''
    def update_control_point_position(event):
        '''
        when the main item is dragged the control points
        follow
        '''
        update_control_points(item)

    def drag_control_point(event):
        item.width = item.lower_right.x + radius - item.x
        item.height = item.lower_right.y + radius - item.y
        item.bounds.width = item.width
        item.bounds.height = item.height

    item.bounds = RectangleDraw(item.canvas,
        item.x, item.y, item.width, item.height,
        fill='', outline=DRAG_CONTROL_STYLE['fill'])
    item.bounds.style['width'] = 2
    item.bounds.update()
    item.lower_right = OvalDraw(item.canvas,
        item.x+item.width-radius, item.y+item.height-radius, radius*2,
        radius*2, **DRAG_CONTROL_STYLE)

    draggable(item, update=update_control_point_position)
    draggable(item.lower_right, update=drag_control_point)
    change_control_point_color(item.lower_right)

def remove_drag_control(item):
    '''
    remove control points
    '''
    item.draggable = False
    item.lower_right.delete()

# TODO
class RoundedRectangleDraw(PolygonDraw):
    def __init__(self, canvas, coords, radius=[2, 2, 2, 2], **kws):
        self.__coords = coords
        self.radius = radius
        PolygonDraw.__init__(self, canvas, self.__coords, **kws)

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

    @property
    def coords(self):
        pts = []
        # NW
        if self.radius[0]:
            cx = self.__coords[0] + self.radius[0]
            cy = self.__coords[1] + self.radius[0]
            for i in range(90, 180):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[0], i))
        else:
            pts.extend([self.__coords[0], self.__coords[1]])
        # SW
        if self.radius[1]:
            cx = self.__coords[0] + self.radius[1]
            cy = self.__coords[3] - self.radius[1]
            for i in range(180, 270):
                pts.extend(self.get_circle_point(cx, cy,
                    self.radius[1], i))
        else:
            pts.extend([self.__coords[0], self.__coords[3]])

        # SE
        if self.radius[2]:
            cx = self.__coords[2] - self.radius[2]
            cy = self.__coords[3] - self.radius[2]
            for i in range(270, 360):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[2],i))
        else:
            pts.extend([self.__coords[2],
                self.__coords[3]])
        # NE
        if self.radius[3]:
            cx = self.__coords[2] - self.radius[3]
            cy = self.__coords[1] + self.radius[3]
            for i in range(0, 90):
                pts.extend(self.get_circle_point(cx,cy,
                    self.radius[3],i))
        else:
            pts.extend([self.__coords[2],
                self.__coords[1]])
        return pts

    @coords.setter
    def coords(self, value):
        self.__coords = value

class ExtendedCanvas(Tkinter.Canvas, object):
    def __init__(self, *args, **kwargs):
        Tkinter.Canvas.__init__(self, *args, **kwargs)

    @property
    def center(self):
        return [self.width/2, self.height/2]

    @property
    def width(self):
        return int(self['width']) - 1

    @width.setter
    def width(self, value):
        self['width'] = value

    @property
    def height(self):
        return int(self['height']) - 1

    @height.setter
    def height(self, value):
        self['height'] = value

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

class IOSCheckbox(ExtendedCanvas):
    pass # TODO

CHECK_MARK=unichr(10003)
class SimpleCheckbox(ExtendedCanvas):
    def __init__(self, parent, checked=False, width=25, height=25):
        ExtendedCanvas.__init__(self,
            parent, width=width,
            height=height,
            bg=parent['bg'],
            relief='flat', bd=0,
            highlightthickness=0)

        self.__bg = RoundedRectangleDraw(self,
            [0, 0, width, height],
            fill='#5cb85c')
        self.__text = TextDraw(self,
            self.center[0], 
            self.center[1],
            CHECK_MARK if checked else '',
            fill='white',
            font=('TkDefaultFont', 12, 'bold'))
        self.bind('<1>', self.__check_click, '+')

    @property
    def checked(self):
        return self.__text.text == CHECK_MARK

    @checked.setter
    def checked(self, value):
        if bool(value):
            self.__text.text = CHECK_MARK
        else:
            self.__text.text = ''

    def __check_click(self, event):
        self.checked = not self.checked

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

        self.__title = TextDraw(canvas, 50, 7 + yoffset, title,
            anchor='nw', font=('TkDefaultFont', 10))
        self.__subtitle = TextDraw(canvas, 50, 22 + yoffset,
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
        self.__rec_bg.style['fill'] = '#cdcdcd'
        self.__rec_bg.update()

    def __mouse_leave(self, evt):
        if self.__selected:
            self.__rec_bg.style['fill'] = '#bbb'
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
    def __init__(self, *args, **kws):
        self.__items = []
        self.item_height = kws.pop('item_height', 40)
        ExtendedCanvas.__init__(self, *args, **kws)

    def add_item(self, title, subtitle=None, icon=None):
        item = ExtendedListboxItem(self, title, subtitle, icon,
            self.item_height, self.item_height * len(self.__items),
            self.desselect_all)
        self.__items.append(item)
        self['scrollregion'] = (0, 0, self.width, self.item_height * len(self.__items))
        return item

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
        self.radius = [2, 2, 2, 2]
        self.level = 1
        self.__bg_color = BG_COLOR
        self.__bd_color = '#aaa'
        self.__fg_color = 'black'

        self.default = kwargs.pop('default', '')
        self.text = kwargs.pop('text', '')
        self.command = kwargs.pop('command', None)

        if self.default == 'active':
            self.__bd_color = '#00aacc'

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

class Text(Tkinter.Text, object):
    def __init__(self, *args, **kws):
        Tkinter.Text.__init__(self, *args, **kws)

    def centralize_text(self):
        self.tag_configure("center", justify='center')
        self.tag_add("center", 1.0, "end")

class MarkDownLabel(Text):
    def __init__(self, master, text='', **kws):
        kws.update(height=kws.get('height', 1))
        self.normal_font = tkFont.Font(size=9)
        self.h1_size = 20
        self.__tag_count = 0
        Text.__init__(self, master, **kws)
        self['state'] = 'disabled'
        self.text = text
        self['highlightthickness'] = 0
        self['relief'] = 'flat'
        self['bg'] = master['bg']


        self.tag_config('normal', font=('TkDefaultFont', 9))
        self.tag_config('bold', font=('TkDefaultFont', 9, 'bold'))
        self.tag_config('italic', font=('TkDefaultFont', 9, 'italic'))
        self.tag_config('h1', font=('TkDefaultFont', 20))
        # mixes
        self.tag_config('bold.italic', font=('TkDefaultFont', 9, 'italic', 'bold'))
        self.tag_config('h1.italic', font=('TkDefaultFont', 20, 'italic'))
        self.tag_config('h1.bold', font=('TkDefaultFont', 20, 'bold'))
        self.tag_config('h1.bold.italic', font=('TkDefaultFont', 20, 'italic', 'bold'))

    @property
    def text(self):
        return self.get(0.0, 'end')

    @text.setter
    def text(self, value):
        self['state'] = 'normal'
        self.delete(0.0, 'end')

        lines = value.split('\n')
        for i in lines:
            self.__write_line(i)

        self['state'] = 'disabled'

    def __write_line(self, line):
        # makes a copy of normal font
        font = tkFont.Font(**self.normal_font.actual())
        if line.split()[0] == '#':
            font['size'] = self.h1_size
            line = ' '.join(line.split()[1:])
        # if is title, cant be a list or other thing
        self.insert_with_font(line, font)
        self.insert('end', '\n')

        # verifying bold and italic

    def __gen_sprite_name(self):
        '''
        generates a random name
        '''
        return ''.join( [random.choice(string.letters) for i in xrange(15)] )

    def insert_with_font(self, text, font):
        '''
        creates a new tag with this font and
        inserts the text with it
        '''
        tag = self.__gen_sprite_name()
        self.tag_config(tag, font=font)
        self.insert('end', text, (tag,))
        self.__tag_count += 1

class CanvasGrid(object):
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.__x = x
        self.__y = y
        self.update()

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
        self.update()

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value
        self.update()

    def __draw_grid(self):
        if (not self.x) or (not self.y):
            return
        for i in range(0, self.canvas.width, self.canvas.width / self.x):
            self.canvas.create_line(i, 0, i, self.canvas.height-1, fill='red',
                tag=('_-_grid-_-'), dash=(5,))
        for i in range(0, self.canvas.height, self.canvas.height / self.y):
            self.canvas.create_line(0, i, self.canvas.width-1, i, fill='red',
                tag=('_-_grid-_-'), dash=(5,))

    def update(self):
        self.canvas.delete('_-_grid-_-')
        self.__draw_grid()

class Entry(Tkinter.Entry, object):
    def __init__(self, *args, **kws):
        self.__placeholder = kws.pop('placeholder', '')
        kws.update(relief='flat',
            border=10,
            insertwidth=1,
            highlightcolor='#aaa',
            highlightthickness=1)
        Tkinter.Entry.__init__(self, *args, **kws)

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

class Scrollbar(ttk.Scrollbar):
    pass

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

class MessageDialog(DefaultDialog):
    def __init__(self, master, title, message):
        self.__message = message
        DefaultDialog.__init__(self, master, title=title)

    def body(self, master):
        mdl = MarkDownLabel(master,
            height=1, width=25,
            text=self.__message)
        mdl.centralize_text()
        mdl.pack(expand='yes', fill='both')
        return mdl

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='left', padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        box.pack()

class MessageBox:
    @staticmethod
    def warning(**kws):
        MessageDialog(kws.get('parent'), kws.get('title', ''), kws.get('message'))

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

class PopUpMenu(Tkinter.Toplevel):
    def __init__(self, master, items, width=500):
        Tkinter.Toplevel.__init__(self, master)
        self.overrideredirect(True)
        self.canvas = ExtendedListbox(self)
        self['width'] = width # TODO fixme

        self.bind('<Escape>', lambda evt: self.destroy(), '+')
        self.focus_force()
        # ver alternativa pra isso:
        # self.bind('<FocusOut>', lambda evt: self.destroy(), '+')

        self.geometry('%dx%d' % (width, len(items)*40))
        self.update_idletasks()
        self.canvas.width = width
        self.canvas.pack(expand='yes', fill='both')

        for i in items:
            self.add_command(i.get('name', ''),
                subtitle=i.get('description', None),
                icon=i.get('icon', None),
                command=i.get('command', None))

        center(self)

    def add_command(self, title, subtitle=None, icon=None, command=None):
        '''
        binds a new command to ExtendedListboxItem, when
        command is called and after that the popup closes
        '''
        item = self.canvas.add_item(title, subtitle, icon)
        def __final_command(evt):
            self.withdraw()
            command(evt)
            self.destroy()
        item.bind('<1>', __final_command, '+')

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()

from newproject import NewProjectWindow
from about import AboutWindow
from scene import AddSceneWindow
from assets import AddSoundAssetWindow, AddImageAssetWindow
from sprite import SpriteImagePropertyWindow