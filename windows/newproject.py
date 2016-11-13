from . import *

class NewProjectWindow(DefaultDialog):
    def __init__(self, master, phaserproject, do_on_end=None):
        self.phaserproject = phaserproject
        self.do_on_end = do_on_end
        DefaultDialog.__init__(self, master, title="New project")
    
    def body(self, master):
        Label(master, text="Project name").grid(sticky='W', row=0, column=0, columnspan=4)
        self.name_entry = Entry(master, width=45)
        self.name_entry.grid(row=1, column=0, columnspan=4)
        self.name_entry.focus_force()
        self.name_entry.insert(0, self.phaserproject.name)

        Label(master, text='Width: ').grid(row=2, column=0, sticky='W')

        self.width = Entry(master, width=4)
        self.width.grid(row=2, column=1, sticky='W')
        self.width.insert(0, str(self.phaserproject.width))

        Label(master, text='Height: ').grid(row=2, column=2, sticky='W')

        self.height = Entry(master, width=4)
        self.height.grid(row=2, column=3, sticky='W')
        self.height.insert(0, str(self.phaserproject.height))

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

        self.phaserproject.width = width
        self.phaserproject.height = height
        self.phaserproject.name = self.name_entry.get()

        if self.do_on_end:
            self.do_on_end(self.phaserproject)
    
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