import tkFileDialog
import tkSimpleDialog
import tkMessageBox
from . import DefaultWindow, default_attrs
from Tkinter import *
import posixpath

class AddAssetWindow(tkSimpleDialog.Dialog):
    def body(self, master):
        # row 1
        Label(master, text="Name", **default_attrs).grid(row=0, column=0)
        self.asset_name = Entry(master)
        self.asset_name.grid(row=0, column=1)

        # row 2
        _path_types = [
            "image",
            "spritesheet",
            "audio"
        ]
        self.assettype = StringVar(master)
        self.assettype.set(_path_types[0])
        Label(master, text="Type", **default_attrs).grid(row=1, column=0)
        self.optmenu = OptionMenu(master, self.assettype,
            *_path_types)
        self.optmenu.grid(sticky='nw', row=1, column=1)

        # row 3
        Label(master, text="Path", **default_attrs).grid(row=2, column=0)
        self.path = Entry(master)
        self.path.grid(row=2, column=1)
        Button(master, text="...", command=self.search_path).grid(row=2, column=2)

        self.output = None
        return self.asset_name # initial focus
    
    def search_path(self):
        '''
        called when user clicks in '...' button
        '''
        filename = tkFileDialog.askopenfilename()
        if filename:
            self.path.delete(0, 'end')
            self.path.insert(0, filename)
    
    def validate(self):
        if not posixpath.isfile(self.path.get()):
            tkMessageBox.showwarning(title='Invalid path', message='Enter a valid path')
            return False
        if not self.asset_name.get():
            tkMessageBox.showwarning(title='Invalid name', message='Enter a name')
            return False
        return True
    
    def apply(self):
        self.output = {
            "path": self.path.get(),
            "type": self.assettype.get(),
            "name": self.asset_name.get()
        }

class AssetsManagerWindow(tkSimpleDialog.Dialog):
    def __init__(self, master, phaserproject):
        self.phaserproject = phaserproject
        tkSimpleDialog.Dialog.__init__(self, master)

    def body(self, master):
        self._top_frame = Frame(master)
        self._top_frame.grid(row=0, column=0, sticky='e')

        self._remove_asset = Button(self._top_frame,
            text='-',
            width=2,
            command=self.__remove_asset_callback).grid(sticky='e',
                row=0,
                column=1)

        Button(self._top_frame,
            text='+',
            width=2,
            command=self.__add_asset_callback).grid(sticky='e',
                row=0,
                column=0)

        self._list = Listbox(master, width=100)
        self._list.grid(row=1, column=0)

        self.__fill_list()
    
    def __fill_list(self):
        for i in self.phaserproject.assets:
            self._list.insert('end', str(i))
    
    def __add_asset_callback(self):
        add_asset = AddAssetWindow(self, title="Add Asset")
        if add_asset.output:
            self._list.insert('end', str(add_asset.output))
            self.phaserproject.assets.append(add_asset.output)
    
    def __remove_asset_callback(self):
        _cur_selection = self._list.curselection()
        if _cur_selection:
            self._list.delete(_cur_selection)
            self.phaserproject.assets.pop(_cur_selection[0])