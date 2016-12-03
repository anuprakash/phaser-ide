from . import *
import posixpath

class AddSoundAssetWindow(DefaultDialog):
    def __init__(self, parent, title=None, path=''):
        self.__path = path
        DefaultDialog.__init__(self, parent, title)

    def body(self, master):
        self.output = None
        Label(master, text="Name").grid(row=0, column=0)
        self.sprite_name = Entry(master)
        self.sprite_name.grid(row=0, column=1)
        self.sprite_name.text = posixpath.basename(self.__path).split('.')[0].lower()
        return self.sprite_name

    def validate(self):
        if not self.sprite_name.get():
            MessageBox.warning(title='Invalid name', message='Enter a valid name')
            return False
        return True

    def apply(self):
        self.output = {
            'name': self.sprite_name.get(),
            'path': self.__path,
            'type': 'music'
        }

class SpriteEditor(DefaultDialog):
    def __init__(self, master, path):
        self.__path = path
        DefaultDialog.__init__(self, master, title='Sprite Editor ' + master.title())

    def body(self, master):
        self.output = None
        self.canvas = ExtendedCanvas(master)
        self.__image = ImageDraw(self.canvas, 0, 0, self.__path, anchor='nw')
        self.canvas.width = self.__image.image.width()
        self.canvas.height = self.__image.image.height()
        self.canvas.pack(expand='yes')

        self._top_frame = Frame(master)
        self._top_frame.pack()

        self._left_frame = Frame(self._top_frame)
        self._left_frame.pack(side='left')

        Label(self._left_frame, text='Width').pack(anchor='nw')
        self.width = Entry(self._left_frame, numbersonly=True, min=1)
        self.width.text = 2
        self.width.pack(anchor='nw')
        self.width.bind('<Any-KeyRelease>', self.__update_grid, '+')

        self._right_frame = Frame(self._top_frame)
        self._right_frame.pack(side='left')

        Label(self._right_frame, text='Height').pack(anchor='nw')
        self.height = Entry(self._right_frame, numbersonly=True, min=1)
        self.height.text = 2
        self.height.pack(anchor='nw')
        self.height.bind('<Any-KeyRelease>', self.__update_grid, '+')

        self.__canvas_grid = CanvasGrid(self.canvas, 2, 2)

        self.autoplay = LabeledSimpleCheckbox(master, text='Autoplay animation', checked=True)
        self.autoplay.pack(expand='yes', anchor='nw')

        self._fr_frame = Frame(master)
        self._fr_frame.pack(expand='yes', anchor='nw')

        self.framerate = Entry(self._fr_frame, width=4, numbersonly=True, min=1)
        self.framerate.text = 1
        self.framerate.pack(anchor='nw', pady=5, padx=5, side='left')
        Label(self._fr_frame, text='Frame rate').pack(expand='yes', anchor='w')

    def __update_grid(self, event):
        try:
            self.__canvas_grid.x = int(self.width.text)
            self.__canvas_grid.y = int(self.height.text)
            self.__canvas_grid.update()
        except ValueError:
            pass

    def apply(self):
        self.output = {
            'sprite_width': int(self.width.text),
            'sprite_height': int(self.height.text),
            'autoplay': self.autoplay.checked,
            'framerate': int(self.framerate.text)
        }

    def validate(self):
        try:
            if (int(self.width.text) <= 0) or (int(self.height.text) <= 0):
                MessageBox.warning(parent=self,
                    title='Wrong size',
                    message='Positive numbers only')
                return False
            return True
        except:
            MessageBox.warning(parent=self, title='Wrong size', message='Digits only (No white spaces)')
            return False

class AddImageAssetWindow(DefaultDialog):
    def __init__(self, parent, title=None, path=''):
        self.__path = path
        DefaultDialog.__init__(self, parent, title)

    def body(self, master):
        self.output = None
        self.sprite_name = Entry(master, placeholder='Name')
        self.sprite_name.grid(row=1, columnspan=2)
        self.sprite_name.text = posixpath.basename(self.__path).split('.')[0].lower()

        self.is_sprite = LabeledSimpleCheckbox(master, text='Is sprite')
        self.is_sprite.grid(row=2, sticky='nw')
        return self.sprite_name

    def validate(self):
        if not self.sprite_name.text:
            MessageBox.warning(parent=self,
                title='Invalid name',
                message='Enter a valid name')
            return False
        return True

    def apply(self):
        self.output = {
            'name': self.sprite_name.get(),
            'path': self.__path,
            'type': 'image'
        }
        if self.is_sprite.checked:
            se = SpriteEditor(self, self.__path)
            if se.output:
                self.output.update(**se.output)
                self.output.update(type='sprite')
            else:
                self.output = None