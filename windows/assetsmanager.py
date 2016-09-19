import tkSimpleDialog
from . import DefaultWindow, default_attrs
from Tkinter import Listbox, Label, Entry, Frame, Button

class AddAssetWindow(tkSimpleDialog.Dialog):
    def body(self, master):
        Label(master, text="Name", **default_attrs).grid(row=0)
        self.asset_name = Entry(master)
        self.asset_name.grid(row=0, column=1)
        return self.asset_name # initial focus
    
    def apply(self):
        first = int(self.asset_name.get())

class AssetsManagerWindow(DefaultWindow):
    def __init__(self, master, phaserproject, do_on_end=None):
        DefaultWindow.__init__(self, master, phaserproject, do_on_end)
        self._top_frame = Frame(self._toplevel)
        self._top_frame.grid(row=0, column=0, sticky='e')

        self._remove_asset = Button(self._top_frame, text='-', width=2)
        self._remove_asset.grid(sticky='e', row=0, column=1)

        Button(self._top_frame,
            text='+',
            width=2,
            command=self._add_asset_callback).grid(sticky='e', row=0, column=0)

        self._list = Listbox(self._toplevel, width=100)
        self._list.grid(row=1, column=0)

        self.__fill_list()
        self.centralize()
    
    def __fill_list(self):
        # fixme: read from 'phaserproject'
        for i in range(10):
            self._list.insert('end', str(i))
    
    def _add_asset_callback(self):
        add_asset = AddAssetWindow(self._toplevel, title="Add Asset")