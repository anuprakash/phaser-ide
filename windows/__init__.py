default_pad = {
    'padx': 5,
    'pady': 5
}

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        cls._instances[cls].focus()
        return cls._instances[cls]

def center(widget):
    widget.update_idletasks()
    sw = int(widget.winfo_screenwidth())
    sh = int(widget.winfo_screenheight())
    ww = int(widget.winfo_width())
    wh = int(widget.winfo_height())
    xpos = (sw / 2) - (ww / 2)
    ypos = (sh / 2) - (wh / 2)
    widget.geometry('%dx%d+%d+%d' % (ww, wh, xpos, ypos))

from newproject import *
from about import *