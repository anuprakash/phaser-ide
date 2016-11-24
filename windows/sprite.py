from . import *

class SpriteImagePropertyWindow(DefaultDialog):
    def __init__(self, master, _dict):
        self.__dict = _dict
        DefaultDialog.__init__(self, master)

    def body(self, master):
        self.output = None
        Label(master, text='x').grid(row=0, column=0)
        self.x = Entry(master, width=4)
        self.x.text = self.__dict.get('x')
        self.x.grid(row=0, column=1)

        Label(master, text='y').grid(row=0, column=2)
        self.y = Entry(master, width=4)
        self.y.text = self.__dict.get('y')
        self.y.grid(row=0, column=3)

        Label(master, text='name:').grid(row=1, column=0)
        self.name = Entry(master, width=20)
        self.name.text = self.__dict.get('name')
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