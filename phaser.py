import core
import ttk
import tkFileDialog
from Tkinter import *
from windows import *

def new_project(*args):
    NewProjectWindow(top, core.PhaserProject())

def open_project(*args):
    filename = tkFileDialog.askopenfilename()
    if filename:
        print 'ok'

def show_about_window():
    AboutWindow(top)

def show_create_manager():
    pass

top = Tk()
top.title('Phaser')
top.state('zoomed')

# parent of all menus
menubar = Menu(top)

# file menu
projectmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Project", menu=projectmenu)
projectmenu.add_command(label="New project", command=new_project)
projectmenu.add_command(label="Open project", command=open_project)
projectmenu.add_command(label="Scene manager", command=show_create_manager)
projectmenu.add_separator()
projectmenu.add_command(label="Quit", command=top.destroy)

# assets menu
assetsmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Assets", menu=assetsmenu)
assetsmenu.add_command(label="Assets manager")

# about menu
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About", command=show_about_window)

# add menu to window
top.config(menu=menubar)
center(top)
top.mainloop()