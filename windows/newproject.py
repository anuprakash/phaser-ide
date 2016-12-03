from . import *

FORMSTRING = '''
Project name@string
Width@int|Height@int
Background color@color
Fullscreen@check
'''

class NewProjectWindow(DefaultDialog):
    def __init__(self, master, _dict=None):
        self._dict = _dict
        self.output = None
        DefaultDialog.__init__(self, master, title='%s Project' % ('Edit' if _dict else 'New'))

    def body(self, master):
        initial_values = [
            '',
            640, 480,
            '#dadada',
            False
        ]
        if self._dict:
            initial_values = [
                self._dict.get('name'),
                self._dict.get('width'), self._dict.get('height'),
                self._dict.get('bgcolor'),
                self._dict.get('fullscreen')
            ]
        self.form = FormFrame(master, FORMSTRING, initial_values=initial_values)
        self.form.grid(sticky='W', row=0, column=0, columnspan=4)

        return self.form.inputs[0]

    def apply(self):
        '''
        called when ok button is pressed
        '''
        values = self.form.get_values()

        self.output = {
            'name': values[0],
            'width': values[1],
            'height': values[2],
            'bgcolor': values[3],
            'fullscreen': values[4]
        }

    def validate(self):
        values = self.form.get_values()
        width = values[1]
        height = values[2]
        if width <= 0 or height <= 0:
            MessageBox.warning(parent=self,
                title='Wrong data',
                message='Invalid width/height')
            return False
        if not values[0]:
            MessageBox.warning(parent=self,
                title='Project title',
                message='Invalid project name')
            return False
        return True