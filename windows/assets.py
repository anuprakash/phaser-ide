from . import *
import posixpath

class AddSoundAssetWindow(DefaultDialog):
    def __init__(self, parent, title=None, path=''):
        self.__path = path
        DefaultDialog.__init__(self, parent, title)

    def body(self, master):
        self.output = None
        Label(master, text="Name").grid(row=0, column=0)
        self.scene_name = Entry(master)
        self.scene_name.grid(row=0, column=1)
        self.scene_name.text = posixpath.basename(self.__path).split('.')[0].lower()
        return self.scene_name

    def validate(self):
        if not self.scene_name.get():
            MessageBox.warning(title='Invalid name', message='Enter a valid name')
            return False
        return True

    def apply(self):
        self.output = {
            'name': self.scene_name.get(),
            'path': self.__path,
            'type': 'music'
        }

class AddImageAssetWindow(DefaultDialog):
    def __init__(self, parent, title=None, path=''):
        self.__path = path
        DefaultDialog.__init__(self, parent, title)

    def body(self, master):
        self.output = None
        Label(master, text='Name').grid(row=0, column=0)
        self.scene_name = Entry(master)
        self.scene_name.grid(row=0, column=1)
        self.scene_name.text = posixpath.basename(self.__path).split('.')[0].lower()
        return self.scene_name

    def validate(self):
        if not self.scene_name.get():
            MessageBox.warning(title='Invalid name', message='Enter a valid name')
            return False
        return True

    def apply(self):
        self.output = {
            'name': self.scene_name.get(),
            'path': self.__path,
            'type': 'image'
        }