from . import *
import json

class NewProjectWindow(DefaultDialog):
    def __init__(self, master, _json=None):
        self.json = _json
        self.output = None
        DefaultDialog.__init__(self, master, title="New project")
    
    def body(self, master):
        Label(master, text="Project name").grid(sticky='W', row=0, column=0, columnspan=4)
        self.name_entry = Entry(master, width=45)
        self.name_entry.grid(row=1, column=0, columnspan=4)
        self.name_entry.focus_force()

        Label(master, text='Width: ').grid(row=2, column=0, sticky='W')

        self.width = Entry(master, width=4)
        self.width.grid(row=2, column=1, sticky='W')

        Label(master, text='Height: ').grid(row=2, column=2, sticky='W')

        self.height = Entry(master, width=4)
        self.height.grid(row=2, column=3, sticky='W')

        if self.json:
            data = json.loads(self.json)
            self.name_entry.insert(0, data.get('name', ''))
            self.width.insert(0, str(data.get('width', '640')))
            self.height.insert(0, str(data.get('height', '480')))
        else:
            self.name_entry.insert(0, '')
            self.width.insert(0, '640')
            self.height.insert(0, '480')
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
            print 'Invalid width or height'

        self.output = json.dumps({
            'name': self.name_entry.get(),
            'width': width,
            'height': height,
            'scenes': '[]',
            'assets': '[]'
        })
    
    def validate(self):
        width, height = 0, 0
        try:
            width = int(self.width.get())
            height = int(self.height.get())
        except:
            MessageBox.warning(title='Wrong data', message='Invalid width/height')
            return False
        if not self.name_entry.get():
            MessageBox.warning(title='Project title', message='Invalid project name')
            return False
        return True