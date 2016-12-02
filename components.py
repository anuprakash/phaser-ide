from windows import *
from windows.sprite import SpriteSheetImagePropertyWindow, SpriteImagePropertyWindow
import random
import string
from PIL import Image
import ImageTk

class GenericComponent(object):
    def __init__(self, ide, name, spritetype):
    	self.ide = ide
    	self.spritetype = spritetype
        self.name = self.__gen_sprite_name()
        self.assetname = name

    def __gen_sprite_name(self):
        '''
        generates a random name
        '''
        return ''.join( [random.choice(string.letters) for i in xrange(15)] )

class GenericImageComponent(GenericComponent, ImageDraw):
    def __init__(self, canvas, x, y, path, ide, name, spritetype):
        GenericComponent.__init__(self, ide, name, spritetype)
        ImageDraw.__init__(self, canvas, x, y, path, anchor='nw')
        self.bind('<3>', self.show_sprite_menu, '+')
        # generates the control points
        drag_control(self)

    def raise_sprite(self, event):
        '''
        called in popup menu
        '''
        self.up()

    def lower_sprite(self, event):
        '''
        called in popup menu
        '''
        self.down()
    
    def get_pop_up_items(self):
        return [
            {
                'name': 'Up',
                'description': 'Puts the sprite in top of others',
                'command': self.raise_sprite,
                'icon': 'icons/up.png'
            },
            {
                'name': 'Down',
                'description': 'Puts the sprite in bottom of others',
                'command': self.lower_sprite,
                'icon': 'icons/down.png'
            },
            {
                'name': 'Centralize',
                'description': 'Centralizes the sprite in middle of canvas',
                'command': self.centralize_sprite,
                'icon': 'icons/center.png'
            },
            {
                'name': 'Properties',
                'description': 'Show/edits the sprite properties',
                'command': self.show_sprite_properties,
                'icon': 'icons/tools.png'
            }
        ]

    def centralize_sprite(self, event=None):
        '''
        called in popup menu
        '''
        self.x = (self.ide.cur_canvas().width / 2) - (self.width / 2)
        self.y = (self.ide.cur_canvas().height / 2) - (self.height / 2)

    def show_sprite_properties(self, event=None):
        '''
        You must override this function for each kind of
        image-sprite
        '''
        raise NotImplementedError

    def show_sprite_menu(self, event=None):
        '''
        called when the user right-click the sprite in canvas
        '''
        pop = PopUpMenu(self.ide, self.get_pop_up_items())

    def update(self):
        '''
        overrides the ImageDraw.update to update the control
        points too
        '''
        ImageDraw.update(self)
        update_control_points(self)

    def up(self):
        '''
        override the ImageDraw.up to make the control points
        up in layers too
        '''
        ImageDraw.up(self)
        self.bounds.up()
        self.lower_right.up()

    def down(self):
        '''
        override the ImageDraw.down to make the control points
        down in layers too
        '''
        self.bounds.down()
        ImageDraw.down(self)
        self.lower_right.up()

    def delete(self):
        ImageDraw.delete(self)
        self.bounds.delete()
        self.lower_right.delete()


class SpriteComponent(GenericImageComponent):
    # canvas, x, y, path, ide, name
    def __init__(self, canvas, x, y, path, ide, name,
            sprite_width, sprite_height, autoplay,
            framerate):
        self.__frames = []
        self.__origin_image = Image.open(path)

        self.framerate = framerate
        # size of each frame in pixels
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.__frame_index = 0
        self.autoplay = autoplay

        GenericImageComponent.__init__(self, canvas, x, y, path, ide, name, 'sprite')

        self.__gen_frames()
        self.image = self.__frames[0]
        self.update()

        self.__start_animation()

    def __start_animation(self):
        self.ide.after(1000 / self.framerate, self.__start_animation)

        if len(self.__frames) == 0 or not self.autoplay:
            return

        self.image = self.__frames[self.__frame_index]
        self.__frame_index += 1
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0

    def __gen_frames(self):
        '''
        crops the image into many images
        '''
        self.__frames = []
        self.__frame_index = 0
        for x in range(0, self.__origin_image.size[0], self.__origin_image.size[0] / self.sprite_width):
            for y in range(0, self.__origin_image.size[1], self.__origin_image.size[1] / self.sprite_height):
                self.__frames.append(
                    ImageTk.PhotoImage(
                        self.__origin_image.crop(
                            (x, y, x+self.__origin_image.size[0] / self.sprite_width,
                                y+self.__origin_image.size[1] / self.sprite_height)
                        )
                    )
                )

    def show_sprite_properties(self, event):
        '''
        shows a window with the sprite properties
        '''
        _dict = {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'sprite_width': self.sprite_width,
            'sprite_height': self.sprite_height,
            'autoplay': self.autoplay,
            'framerate': self.framerate
        }
        sipw = SpriteSheetImagePropertyWindow(self.ide, _dict)
        if sipw.output:
            self.x = sipw.output.get('x')
            self.y = sipw.output.get('y')
            self.name = sipw.output.get('name')
            self.autoplay = sipw.output.get('autoplay')
            self.framerate = sipw.output.get('framerate')
            self.sprite_width = sipw.output.get('sprite_width')
            self.sprite_height = sipw.output.get('sprite_height')
            self.__gen_frames()


class ImageComponent(GenericImageComponent):
    def __init__(self, canvas, x, y, path, ide, name):
        GenericImageComponent.__init__(self, canvas, x, y, path, ide, name, 'image')

    def show_sprite_properties(self, event):
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
