'''
the windows defined here are used to show properties
when the user right-clicks in sprite
'''
import boring.dialog
import boring.form

SPRITE_IMAGE_FORMSTRING = '''
Name@string
X@int|Y@int
'''
class SpriteImagePropertyWindow(boring.dialog.DefaultDialog):
    def __init__(self, master, _dict):
        self._dict = _dict
        boring.dialog.DefaultDialog.__init__(
            self, master
        )

    def body(self, master):
        self.output = None

        self.form = boring.form.FormFrame(
            master,
            SPRITE_IMAGE_FORMSTRING,
            initial_values=[
                self._dict.get('name'),
                self._dict.get('x'),
                self._dict.get('y')
            ],
            title='Sprite Properties'
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
Autoplay animation@check
Frame rate (fps)@int
'''
class SpriteSheetImagePropertyWindow(SpriteImagePropertyWindow):
    def body(self, master):
        SpriteImagePropertyWindow.body(self, master)

        self.spriteform = boring.form.FormFrame(
            master,
            SPRITESHEET_FORMSTRING,
            initial_values=[
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

        if values[1] <= 0: # framerate
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
            autoplay=values[0],
            framerate=values[1]
        )