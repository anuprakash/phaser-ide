'''
the windows defined here are used to show properties
when the user right-clicks in sprite
'''
from . import *

SPRITE_IMAGE_FORMSTRING = '''
Name@string
X@int|Y@int
'''
class SpriteImagePropertyWindow(DefaultDialog):
    def __init__(self, master, _dict):
        self._dict = _dict
        DefaultDialog.__init__(self, master)

    def body(self, master):
        self.output = None

        self.form = FormFrame(
            master,
            SPRITE_IMAGE_FORMSTRING,
            initial_values=[
                self._dict.get('name'),
                self._dict.get('x'),
                self._dict.get('y')
            ]
        )
        self.form.grid(pady=5, padx=10)

        return self.form.inputs[0]

    def validate(self):
        if self.form.values[0].strip() == '':
            MessageBox.warning(parent=self,
                title='Wrong data',
                message='Invalid name')
            return False
        return True

    def apply(self):
        values = self.form.values
        self.output = {
            'name': values[0],
            'x': values[1],
            'y': values[2]
        }


SPRITESHEET_FORMSTRING = '''
Sprite Width@int|Sprite height@int
Autoplay animation@check
Frame rate@int
'''
class SpriteSheetImagePropertyWindow(SpriteImagePropertyWindow):
    def body(self, master):
        SpriteImagePropertyWindow.body(self, master)

        self.spriteform = FormFrame(
            master,
            SPRITESHEET_FORMSTRING,
            initial_values=[
                self._dict.get('sprite_width'),
                self._dict.get('sprite_height'),
                self._dict.get('autoplay'),
                self._dict.get('framerate')
            ]
        )
        self.spriteform.grid(pady=5, padx=10)
    
    def validate(self):
        _return = SpriteImagePropertyWindow.validate(self)
        if not _return:
            return False

        values = self.spriteform.values
        if values[0] <= 0 or values[1] <= 0:
            MessageBox.warning(
                parent=self,
                title='Wrong data',
                message='Invalid x/y'
            )
            return False

        if values[3] <= 0:
            MessageBox.warning(
                parent=self,
                title='Wrong data',
                message='Invalid framerate'
            )
            return False
        return True

    def apply(self):
        SpriteImagePropertyWindow.apply(self)
        values = self.spriteform.values
        self.output.update(
            sprite_width=values[0],
            sprite_height=values[1],
            autoplay=values[2],
            framerate=values[3]
        )