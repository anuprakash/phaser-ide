from . import *
import json

class NewProjectWindow(DefaultDialog):
    def __init__(self, master, _dict=None):
        self._dict = _dict
        self.output = None
        DefaultDialog.__init__(self, master, title='%s Project' % ('Edit' if _dict else 'New'))
    
    def body(self, master):
        Label(master, text="Project name").grid(sticky='W', row=0, column=0, columnspan=4)
        self.name_entry = Entry(master, width=45)
        self.name_entry.grid(row=1, column=0, columnspan=4, pady=2, padx=2)
        self.name_entry.focus_force()

        Label(master, text='Width: ').grid(row=2, column=0, sticky='W')

        self.width = Entry(master, width=4, numbersonly=True, min=1)
        self.width.grid(row=2, column=1, sticky='W')

        Label(master, text='Height: ').grid(row=2, column=2, sticky='W')

        self.height = Entry(master, width=4, numbersonly=True, min=1)
        self.height.grid(row=2, column=3, sticky='W')

        Label(master, text='Background color').grid(row=3, column=0, sticky='NW')
        self.bgcolor = ColorChooser(master, '#dadada', height=30)
        self.bgcolor.grid(row=4, column=0, columnspan=4)

        self.fullscreen = LabeledSimpleCheckbox(master, text='Fullscreen')
        self.fullscreen.grid(row=5, column=0, columnspan=2, sticky='w')

        if self._dict:
            self.name_entry.text = self._dict.get('name', '')
            self.width.text = str(self._dict.get('width', '640'))
            self.height.text = str(self._dict.get('height', '480'))
            self.bgcolor.color = self._dict.get('bgcolor', '#dadada')
            self.fullscreen.checked = self._dict.get('fullscreen', False)
        else:
            self.name_entry.text = ''
            self.width.text = 640
            self.height.text = 480
        return self.name_entry
    
    def apply(self):
        '''
        called when ok button is pressed
        '''
        width, height = 0, 0
        try:
            width = int(self.width.get())
            height = int(self.height.get())
        except:
            print('Invalid width or height')

        self.output = {
            'name': self.name_entry.get(),
            'width': width,
            'height': height,
            'bgcolor': self.bgcolor.color,
            'fullscreen': self.fullscreen.checked
        }
    
    def validate(self):
        width, height = 0, 0
        try:
            width = int(self.width.get())
            height = int(self.height.get())
        except:
            MessageBox.warning(parent=self,
                title='Wrong data',
                message='Invalid width/height')
            return False
        if not self.name_entry.get():
            MessageBox.warning(parent=self,
                title='Project title',
                message='Invalid project name')
            return False
        return True