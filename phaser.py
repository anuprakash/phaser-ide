import core
import tkFileDialog
import tkMessageBox
from Tkinter import *
from windows import *

CURRENT_PROJECT = None

def new_project(*args):
    global CURRENT_PROJECT
    CURRENT_PROJECT = core.PhaserProject()
    NewProjectWindow(top, CURRENT_PROJECT)

def open_project(*args):
    filename = tkFileDialog.askopenfilename()
    if filename:
        print 'ok'

def show_about_window():
    AboutWindow(top)

def show_create_manager():
    pass

def show_assets_manager():
    if CURRENT_PROJECT:
        AssetsManagerWindow(top, CURRENT_PROJECT)
    else:
        tkMessageBox.showwarning(title='No project found', message='No project found')

top = Tk()
top.title('Phaser')
try:
	top.state('zoomed')
except:
	top.attributes('-zoomed', 1)

# parent of all menus
menubar = Menu(top, relief=FLAT)

# file menu
projectmenu = Menu(menubar, tearoff=0, relief=FLAT)
menubar.add_cascade(label="Project", menu=projectmenu)
projectmenu.add_command(label="New project", command=new_project)
projectmenu.add_command(label="Open project", command=open_project)
projectmenu.add_command(label="Scene manager", command=show_create_manager)
projectmenu.add_separator()
projectmenu.add_command(label="Quit", command=top.destroy)

# assets menu
# fixme: add tile options etc
assetsmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Assets", menu=assetsmenu)
assetsmenu.add_command(label="Assets manager", command=show_assets_manager)

# settings menu
settingsmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Settings", menu=settingsmenu)
settingsmenu.add_command(label="Editor Settings", command=lambda *args: SettingsWindow(top))

# about menu
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About", command=show_about_window)

# add menu to window
top.config(menu=menubar)
center(top)
top.mainloop()