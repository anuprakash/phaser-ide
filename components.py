from windows import *
import random
import string
from PIL import Image
import ImageTk

class GenericComponent(object):
    def __init__(self, ide, name):
    	self.ide = ide
        self.name = self.__gen_sprite_name()
        self.assetname = name

    def __gen_sprite_name(self):
        '''
        generates a random name
        '''
        return ''.join( [random.choice(string.letters) for i in xrange(15)] )

class SpriteComponent(GenericComponent, ImageDraw):
    def __init__(self, canvas, x, y, path, **kws):
        self.__frames = []
        self.__origin_image = Image.open(path)

        self.framerate = kws.pop('framerate')
        # size of each frame in pixels
        self.sprite_width = self.__origin_image.size[0] / kws.pop('sprite_width')
        self.sprite_height = self.__origin_image.size[1] / kws.pop('sprite_height')
        self.__frame_index = 0
        self.autoplay = kws.pop('autoplay')

        GenericComponent.__init__(self, kws.pop('ide'), kws.pop('name'))
        ImageDraw.__init__(self, canvas, x, y, path, **kws)

        # generates the control points
        drag_control(self)
        self.bind('<3>', self.__show_sprite_menu, '+')

        self.__gen_frames()
        self.image = self.__frames[0]
        self.update()

        if self.autoplay:
            self.__start_animation()

    def __start_animation(self):
        self.image = self.__frames[self.__frame_index]
        self.__frame_index += 1
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0
        self.ide.after(1000 / self.framerate, self.__start_animation)

    def __gen_frames(self):
        self.__frames = []
        for x in range(0, self.__origin_image.size[0], self.sprite_width):
            for y in range(0, self.__origin_image.size[1], self.sprite_height):
                self.__frames.append( ImageTk.PhotoImage(self.__origin_image.crop((x, y, x+self.sprite_width, y+self.sprite_height))) )

    def __show_sprite_menu(self, event):
        '''
        called when the user right-click the sprite in canvas
        '''
        pop = PopUpMenu(self.ide, [
            {
                'name': 'Up',
                'description': 'Puts the sprite in top of others',
                'command': self.__raise_sprite,
                'icon': 'icons/up.png'
            },
            {
                'name': 'Down',
                'description': 'Puts the sprite in bottom of others',
                'command': self.__lower_sprite,
                'icon': 'icons/down.png'
            },
            {
                'name': 'Centralize',
                'description': 'Centralizes the sprite in middle of canvas',
                'command': self.__centralize_sprite,
                'icon': 'icons/center.png'
            },
            {
                'name': 'Properties',
                'description': 'Show/edits the sprite properties',
                'command': self.__show_sprite_properties,
                'icon': 'icons/tools.png'
            }
        ])

    def __raise_sprite(self, event):
        self.up()

    def __lower_sprite(self, event):
        self.down()

    def __show_sprite_properties(self, event):
        '''
        shows a window with the sprite properties
        '''
        _dict = {
            'name': self.name,
            'x': self.x,
            'y': self.y
        }
        sipw = SpriteImagePropertyWindow(self.ide, _dict)
        if sipw.output:
            self.x = sipw.output.get('x')
            self.y = sipw.output.get('y')
            self.name = sipw.output.get('name')

    def __centralize_sprite(self, event):
        '''
        puts the sprite in the middle of canvas
        '''
        self.x = (self.ide.cur_canvas().width / 2) - (self.width / 2)
        self.y = (self.ide.cur_canvas().height / 2) - (self.height / 2)

    def update(self):
        ImageDraw.update(self)
        update_control_points(self)

    def up(self):
        ImageDraw.up(self)
        self.bounds.up()
        self.lower_right.up()

    def down(self):
        self.bounds.down()
        ImageDraw.down(self)
        self.lower_right.up()

class ImageComponent(GenericComponent, ImageDraw):
    def __init__(self, *args, **kws):
        GenericComponent.__init__(self, kws.pop('ide'), kws.pop('name'))
        ImageDraw.__init__(self, *args, **kws)

        # generates the control points
        drag_control(self)
        self.bind('<3>', self.__show_sprite_menu, '+')

    def __show_sprite_menu(self, event):
    	'''
        called when the user right-click the sprite in canvas
        '''
        pop = PopUpMenu(self.ide, [
            {
                'name': 'Up',
                'description': 'Puts the sprite in top of others',
                'command': self.__raise_sprite,
                'icon': 'icons/up.png'
            },
            {
                'name': 'Down',
                'description': 'Puts the sprite in bottom of others',
                'command': self.__lower_sprite,
                'icon': 'icons/down.png'
            },
            {
                'name': 'Centralize',
                'description': 'Centralizes the sprite in middle of canvas',
                'command': self.__centralize_sprite,
                'icon': 'icons/center.png'
            },
            {
                'name': 'Properties',
                'description': 'Show/edits the sprite properties',
                'command': self.__show_sprite_properties,
                'icon': 'icons/tools.png'
            }
        ])

    def __raise_sprite(self, event):
        self.up()

    def __lower_sprite(self, event):
        self.down()

    def __show_sprite_properties(self, event):
        '''
        shows a window with the sprite properties
        '''
        _dict = {
            'name': self.name,
            'x': self.x,
            'y': self.y
        }
        sipw = SpriteImagePropertyWindow(self.ide, _dict)
        if sipw.output:
            self.x = sipw.output.get('x')
            self.y = sipw.output.get('y')
            self.name = sipw.output.get('name')

    def __centralize_sprite(self, event):
        '''
        puts the sprite in the middle of canvas
        '''
        self.x = (self.ide.cur_canvas().width / 2) - (self.width / 2)
        self.y = (self.ide.cur_canvas().height / 2) - (self.height / 2)

    def update(self):
        ImageDraw.update(self)
        update_control_points(self)

    def up(self):
        ImageDraw.up(self)
        self.bounds.up()
        self.lower_right.up()

    def down(self):
        self.bounds.down()
        ImageDraw.down(self)
        self.lower_right.up()