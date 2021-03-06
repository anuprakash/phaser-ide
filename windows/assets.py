import boring.dialog
import boring.draw
import boring.form
import boring.widgets
import posixpath
import boring.drawwidgets

class AddSoundAssetWindow(boring.dialog.DefaultDialog):
    def __init__(self, parent, title=None, path=''):
        self.__path = path
        boring.dialog.DefaultDialog.__init__(self, parent, title)

    def body(self, master):
        self.output = None
        boring.widgets.Label(master, text="Name").grid(row=0, column=0)
        self.sprite_name = boring.widgets.Entry(master)
        self.sprite_name.grid(row=0, column=1)
        self.sprite_name.text = posixpath.basename(self.__path).split('.')[0].lower()
        return self.sprite_name

    def validate(self):
        if not self.sprite_name.get():
            boring.dialog.MessageBox.warning(title='Invalid name', message='Enter a valid name')
            return False
        return True

    def apply(self):
        self.output = {
            'name': self.sprite_name.get(),
            'path': self.__path,
            'type': 'music'
        }

SPRITE_FORMSTRING = '''
Width@int|Height@int
'''

class SpriteEditor(boring.dialog.DefaultDialog):
    def __init__(self, master, path):
        self.__path = path
        boring.dialog.DefaultDialog.__init__(self, master, title='Sprite Editor ' + master.title())

    def body(self, master):
        self.output = None
        self.canvas = boring.widgets.ExtendedCanvas(master)
        self.__image = boring.draw.ImageDraw(
            self.canvas, 0, 0,
            self.__path, anchor='nw'
        )
        self.canvas.width = self.__image.image.width()
        self.canvas.height = self.__image.image.height()
        self.canvas.pack(expand='yes')

        self.form = boring.form.FormFrame(master, SPRITE_FORMSTRING, initial_values=[2, 2, True, 1])
        self.form.pack(pady=10, padx=10)

        # with and height binds
        self.form.inputs[0].bind('<Any-KeyRelease>', self.__update_grid, '+')
        self.form.inputs[1].bind('<Any-KeyRelease>', self.__update_grid, '+')

        self.__canvas_grid = boring.drawwidgets.CanvasGrid(self.canvas, 2, 2)

    def __update_grid(self, event):
        try:
            self.__canvas_grid.x = self.form.values[0]
            self.__canvas_grid.y = self.form.values[1]
            self.__canvas_grid.update()
        except ValueError:
            pass

    def apply(self):
        values = self.form.values
        self.output = {
            'sprite_width': values[0],
            'sprite_height': values[1]
        }

    def validate(self):
        try:
            if (self.form.values[0] <= 0) or (self.form.inputs[1] <= 0):
                boring.dialog.MessageBox.warning(
                    parent=self,
                    title='Wrong size',
                    message='Positive numbers only'
                )
                return False
            return True
        except:
            boring.dialog.MessageBox.warning(
                parent=self, title='Wrong size',
                message='Digits only (No white spaces)'
            )
            return False

IMAGE_ASSET_FORMSTRING = '''
Name@string
Is sprite@check
'''
class AddImageAssetWindow(boring.dialog.DefaultDialog):
    def __init__(self, parent, title=None, path=''):
        self.__path = path
        boring.dialog.DefaultDialog.__init__(
            self, parent, title
        )

    def body(self, master):
        self.output = None
        self.form = boring.form.FormFrame(
            master, IMAGE_ASSET_FORMSTRING
        )
        self.form.grid(pady=10, padx=10)

        return self.form.inputs[0]

    def validate(self):
        if not self.form.values[0]:
            boring.dialog.MessageBox.warning(parent=self,
                title='Invalid name',
                message='Enter a valid name')
            return False
        return True

    def apply(self):
        values = self.form.values
        self.output = {
            'name': values[0],
            'path': self.__path,
            'type': 'image'
        }
        if self.form.values[1]: # is sprite = true
            se = SpriteEditor(self, self.__path)
            if se.output:
                self.output.update(**se.output)
                self.output.update(type='sprite')
            else:
                self.output = None