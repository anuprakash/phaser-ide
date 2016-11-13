import core
import tkFileDialog
import Tkinter
from windows import *

CURRENT_PROJECT = None

def new_project(*args):
    npw = NewProjectWindow(top)
    if npw.output:
        global CURRENT_PROJECT
        CURRENT_PROJECT = core.PhaserProject()
        CURRENT_PROJECT.fill_from_json(npw.output)

def open_project(*args):
    filename = tkFileDialog.askopenfilename()
    if filename:
        f = open(filename)
        content = f.read()
        f.close()
        global CURRENT_PROJECT
        CURRENT_PROJECT = core.PhaserProject()
        CURRENT_PROJECT.fill_from_json(content)

def save_project(*args):
    fn = tkFileDialog.asksaveasfilename()
    if fn:
        f = open(fn, 'w')
        f.write(CURRENT_PROJECT.get_json())
        f.close()

def show_about_window():
    AboutWindow(top)

def show_assets_manager():
    if CURRENT_PROJECT:
        amw = AssetsManagerWindow(top, CURRENT_PROJECT.get_assets_json())
        if amw.output:
            CURRENT_PROJECT.load_assets_from_json(amw.output)
    else:
        MessageBox.warning(title='No project found', message='No project found')

top = Tkinter.Tk()
top.title('Phaser')
top['bg'] = BG_COLOR
top.geometry('%dx%d' % (1200, 600))
center(top)

# parent of all menus
menubar = Tkinter.Menu(top, relief=Tkinter.FLAT)

## scene manager
def _add_scene_btn_handler(*args):
    if CURRENT_PROJECT:
        asw = AddSceneWindow(top, title="Add Asset")
        if asw.output:
            CURRENT_PROJECT.scenes.append(core.PhaserScene(asw.output))
    else:
        MessageBox.warning(title='No project found', message='No project found')

def _del_scene_btn_handler(*args):
    if CURRENT_PROJECT:
        pass # TODO
    else:
        MessageBox.warning(title='No project found', message='No project found')

left_frame = Frame(top)
left_frame_top = Frame(left_frame)
scene_manager = Listbox(left_frame)

def _add_scene_btn_handler(*args):
    if CURRENT_PROJECT:
        asw = AddSceneWindow(top, title="Add Asset")
        if asw.output:
            try:
                CURRENT_PROJECT.add_scene_from_json(asw.output)
                scene_manager.insert('end', CURRENT_PROJECT.scenes[-1].name)
            except core.DuplicatedSceneNameException:
                MessageBox.warning(title='DuplicatedSceneNameException', message='a scene in project already contains this name')
    else:
        MessageBox.warning(title='No project found', message='No project found')

def _del_scene_btn_handler(*args):
    if CURRENT_PROJECT:
        _cur_selection = scene_manager.curselection()
        if _cur_selection:
            scene_name = scene_manager.get(_cur_selection)
            CURRENT_PROJECT.remove_scene_from_name(scene_name)
            scene_manager.delete(_cur_selection)
    else:
        MessageBox.warning(title='No project found', message='No project found')

add_scene_btn = Button(left_frame_top, text='+', width=20, command=_add_scene_btn_handler)
del_scene_btn = Button(left_frame_top, text='-', width=20, command=_del_scene_btn_handler)

Label(left_frame_top, text='Scenes').pack(anchor='nw',
    side='left')
add_scene_btn.pack(side='right', anchor='ne', padx=1)
del_scene_btn.pack(side='right', anchor='ne', padx=1)
left_frame_top.pack(anchor='nw', padx=5, pady=5, fill='both')
scene_manager.pack(side='left', expand='yes', fill='y', anchor='nw')
left_frame.pack(side='left', expand='yes', fill='y', anchor='nw')


## save operations
def new_project(*args):
    npw = NewProjectWindow(top)
    if npw.output:
        global CURRENT_PROJECT
        CURRENT_PROJECT = core.PhaserProject()
        CURRENT_PROJECT.fill_from_json(npw.output)
        scene_manager.delete(0, 'end')

def open_project(*args):
    filename = tkFileDialog.askopenfilename()
    if filename:
        f = open(filename)
        content = f.read()
        f.close()
        global CURRENT_PROJECT
        CURRENT_PROJECT = core.PhaserProject()
        CURRENT_PROJECT.fill_from_json(content)
        scene_manager.delete(0, 'end')

# file menu
projectmenu = Tkinter.Menu(menubar, tearoff=0, relief=Tkinter.FLAT)
menubar.add_cascade(label="Project", menu=projectmenu)
projectmenu.add_command(label="New project", command=new_project)
projectmenu.add_command(label="Open project", command=open_project)
projectmenu.add_command(label="Save project as", command=save_project)
projectmenu.add_separator()
projectmenu.add_command(label="Quit", command=top.destroy)

# assets menu
# fixme: add tile options etc
assetsmenu = Tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Assets", menu=assetsmenu)
assetsmenu.add_command(label="Assets manager", command=show_assets_manager)

# settings menu
settingsmenu = Tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Settings", menu=settingsmenu)
settingsmenu.add_command(label="Editor Settings", command=lambda *args: SettingsWindow(top))

# about menu
helpmenu = Tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About", command=show_about_window)

# add menu to window
top.config(menu=menubar)
center(top)
top.mainloop()