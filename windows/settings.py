import ttk
import tkSimpleDialog
from . import default_attrs

class SettingsWindow(tkSimpleDialog.Dialog):
    def body(self, master):
        ttk.Label(master, text="TTK Theme", **default_attrs).grid(row=0)
        self.asset_name = ttk.Entry(master)
        self.asset_name.grid(row=0, column=1)
        return self.asset_name # initial focus
    
    def apply(self):
        first = int(self.asset_name.get())