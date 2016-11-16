import core
import tkFileDialog
import Tkinter
from windows import *

CURRENT_PROJECT = None

top = Tkinter.Tk()
ttk.Style().theme_use('clam')
top.title('Phaser')
top['bg'] = BG_COLOR
top.geometry('%dx%d' % (1200, 600))
center(top)

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
        amw = AssetsManagerWindow(top, CURRENT_PROJECT.get_assets_dict())
        if amw.output:
            CURRENT_PROJECT.load_assets_from_dict(amw.output)
    else:
        MessageBox.warning(title='No project found', message='No project found')

# list with all canvas of all scenes
CANVASES = {}
ACTUAL_CANVAS = None

# parent of all menus
menubar = Tkinter.Menu(top, relief=Tkinter.FLAT)

canvas_frame = Frame(top)

## scene manager
left_frame = Frame(top)
left_frame_top = Frame(left_frame)
scene_manager = Listbox(left_frame)

def __on_select_scene(*args):
    '''
    called when the user clicks in a scene
    in scene manager
    '''
    global ACTUAL_CANVAS
    _cur_selection = scene_manager.curselection()
    if _cur_selection:
        scene_name = scene_manager.get(_cur_selection)
        if (scene_name != ACTUAL_CANVAS and ACTUAL_CANVAS != None) or ACTUAL_CANVAS == None:
            if ACTUAL_CANVAS:
                CANVASES[ACTUAL_CANVAS].pack_forget()
            ACTUAL_CANVAS = scene_name
            CANVASES[ACTUAL_CANVAS].pack()
scene_manager.bind('<<ListboxSelect>>', __on_select_scene)

def _add_scene_btn_handler(*args):
    global ACTUAL_CANVAS
    if CURRENT_PROJECT:
        asw = AddSceneWindow(top, title="Add Asset")
        if asw.output:
            try:
                CURRENT_PROJECT.add_scene_from_json(asw.output)
                scene_manager.insert('end', CURRENT_PROJECT.scenes[-1].name)
                ca = Canvas(canvas_frame,
                    width=CURRENT_PROJECT.width,
                    height=CURRENT_PROJECT.height)
                ca.pack(anchor='sw', side='left')
                CANVASES[asw.output['name']] = ca
                ca.create_text(10,10,text=asw.output['name'])
                if ACTUAL_CANVAS:
                    CANVASES[ACTUAL_CANVAS].pack_forget()
                ACTUAL_CANVAS = asw.output['name']
                # put focus in actual canvas
                scene_manager.selection_clear(0, 'end')
                scene_manager.select_set(len(CANVASES.keys())-1)
            except core.DuplicatedSceneNameException:
                MessageBox.warning(
                    title='DuplicatedSceneNameException',
                    message='a scene in project already contains this name')
    else:
        MessageBox.warning(title='No project found', message='No project found')

def _del_scene_btn_handler(*args):
    global ACTUAL_CANVAS
    if CURRENT_PROJECT:
        _cur_selection = scene_manager.curselection()
        if _cur_selection:
            scene_name = scene_manager.get(_cur_selection)
            if OkCancel(top,
                'The scene %s will be delete. Are you sure?' % (scene_name),
                title='Are you sure?').output:

                CURRENT_PROJECT.remove_scene_from_name(scene_name)
                scene_manager.delete(_cur_selection)
                CANVASES[scene_name].pack_forget()
                del CANVASES[scene_name]
                ACTUAL_CANVAS = None
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

left_frame.pack(side='left', fill='y')
canvas_frame.pack(expand='yes')

## save operations
def new_project(*args):
    npw = NewProjectWindow(top)
    if npw.output:
        global CURRENT_PROJECT
        CURRENT_PROJECT = core.PhaserProject()
        CURRENT_PROJECT.fill_from_dict(npw.output)
        # clearing the scene listbox
        scene_manager.delete(0, 'end')
        top.title('Phaser - %s' % (npw.output['name']))

# TODO: remove json loading
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
projectmenu.add_command(label="Open project TODO", command=open_project)
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