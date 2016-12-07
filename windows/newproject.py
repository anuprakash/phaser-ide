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
        DefaultDialog.__init__(self, master)

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
        self.form = FormFrame(master, FORMSTRING, initial_values=initial_values, title='%s Project' % ('Edit' if self._dict else 'New'))
        self.form.grid(pady=10, padx=10)

        return self.form.inputs[0]

    def apply(self):
        '''
        called when ok button is pressed
        '''
        self.output = {
            'name': self.form.values[0],
            'width': self.form.values[1],
            'height': self.form.values[2],
            'bgcolor': self.form.values[3],
            'fullscreen': self.form.values[4]
        }

    def validate(self):
        width = self.form.values[1]
        height = self.form.values[2]
        if width <= 0 or height <= 0:
            MessageBox.warning(parent=self,
                title='Wrong data',
                message='Invalid width/height')
            return False
        if not self.form.values[0]:
            MessageBox.warning(parent=self,
                title='Project title',
                message='Invalid project name')
            return False
        return True