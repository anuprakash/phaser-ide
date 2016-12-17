# widgets

import boring.widgets

class KeyboardSensorWidget(boring.widgets.Button):
    def __init__(self, *args, **kws):
        self.__key = kws.pop('key', None)
        self.__keycode = kws.pop('keycode', None)

        kws.update(
            fgcolor='#aaa'
        )
        self.__receive = False
        boring.widgets.Button.__init__(self, *args, **kws)

        self.bind('<1>', self.__click, '+')
        self.bind('<Any-Key>', self.__any_key, '+')

    def __click(self, event):
        self.text = 'Press a key'
        self.__receive = True
        self.focus_force()

    def __any_key(self, event):
        if self.__receive:
            self.__key = event.keysym
            self.__keycode = event.keycode
            self.__receive = False
            self.text = self.__key

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = unicode(value)

    @property
    def value(self):
        return self.key