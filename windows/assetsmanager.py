import ttk
from . import DefaultWindow

class AssetsManagerWindow(DefaultWindow):
    def __init__(self, master, phaserproject, do_on_end=None):
        DefaultWindow.__init__(self, master, phaserproject, do_on_end=None)