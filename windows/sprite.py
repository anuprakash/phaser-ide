'''
the windows defined here are used to show properties
when the user right-clicks in sprite
'''
from . import *

class SpriteImagePropertyWindow(DefaultDialog):
    def __init__(self, master, _dict):
        self._dict = _dict
        DefaultDialog.__init__(self, master)

    def body(self, master):
        self.output = None
        Label(master, text='x').grid(row=0, column=0)
        self.x = Entry(master, width=4, numbersonly=True, min=1)
        self.x.text = self._dict.get('x')
        self.x.grid(row=0, column=1)

        Label(master, text='y').grid(row=0, column=2)
        self.y = Entry(master, width=4, numbersonly=True, min=1)
        self.y.text = self._dict.get('y')
        self.y.grid(row=0, column=3)

        Label(master, text='name:').grid(row=1, column=0)
        self.name = Entry(master, width=20)
        self.name.text = self._dict.get('name')
        self.name.grid(row=1, column=1, columnspan=3)
        return self.x

    def validate(self):
        try:
            int(self.x.text)
            int(self.y.text)
        except:
            MessageBox.warning(parent=self,
                title='Wrong data',
                message='Invalid x/y')
            return False
        if self.name.text.strip() == '':
            MessageBox.warning(parent=self,
                title='Wrong data',
                message='Invalid name')
            return False
        return True

    def apply(self):
        self.output = {
            'x': int(self.x.text),
            'y': int(self.y.text),
            'name': self.name.text
        }

class SpriteSheetImagePropertyWindow(SpriteImagePropertyWindow):
    def body(self, master):
        SpriteImagePropertyWindow.body(self, master)

        Label(master, text='sprite width').grid(row=2, column=0)
        self.sprite_width = Entry(master, width=4, numbersonly=True, min=1)
        self.sprite_width.text = self._dict.get('sprite_width')
        self.sprite_width.grid(row=2, column=1)

        Label(master, text='sprite height').grid(row=3, column=0)
        self.sprite_height = Entry(master, width=4, numbersonly=True, min=1)
        self.sprite_height.text = self._dict.get('sprite_height')
        self.sprite_height.grid(row=3, column=1)

        self._check_frame = Frame(master)
        self._check_frame.grid(row=4, column=0, columnspan=2)

        self.autoplay = SimpleCheckbox(self._check_frame, checked=self._dict.get('autoplay'))
        self.autoplay.pack(anchor='nw', pady=5, padx=5, side='left')
        Label(self._check_frame, text='Autoplay animation').pack(expand='yes', anchor='w')

        Label(master, text='Frame rate').grid(row=5, column=0)
        self.framerate = Entry(master, width=4, numbersonly=True, min=1)
        self.framerate.text = self._dict.get('framerate')
        self.framerate.grid(row=5, column=1)
    
    def validate(self):
        _return = SpriteImagePropertyWindow.validate(self)
        if not _return:
            return False

        try:
            int(self.sprite_width.text)
            int(self.sprite_height.text)
            int(self.framerate.text)
        except:
            MessageBox.warning(parent=self,
                title='Wrong data',
                message='Invalid sprite width/height')
            return False
        if int(self.framerate.text) <= 0:
            return False
        return True

    def apply(self):
        SpriteImagePropertyWindow.apply(self)
        self.output.update(
            sprite_width=int(self.sprite_width.text),
            sprite_height=int(self.sprite_height.text),
            autoplay=self.autoplay.checked,
            framerate=int(self.framerate.text)
        )