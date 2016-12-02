import core
import tkFileDialog
import Tkinter
from windows import *
import components as comp
import posixpath
import importlib

VErSIOn = 'alpha'

class PhaserEditor(Tkinter.Tk):
    def __init__(self):
        self.current_project = None
        # stores the canvas itself
        # the key is the scene name
        self.canvases = {}
        # stores all sprite of each canvas
        # the key is the scene name
        self.sprite_canvases = {}
        self.actual_canvas = None

        Tkinter.Tk.__init__(self)
        ttk.Style().theme_use('clam')
        self.title('Phaser - %s' % (VErSIOn))
        self['bg'] = BG_COLOR
        self.geometry('%dx%d' % (1200, 600))

        # parent of all menus
        self.menubar = Tkinter.Menu(self, relief=Tkinter.FLAT)
        # file menu
        self.projectmenu = Tkinter.Menu(self.menubar, tearoff=0, relief=Tkinter.FLAT)
        self.menubar.add_cascade(label='Project', menu=self.projectmenu)
        self.projectmenu.add_command(label='New project', command=self.new_project)
        # TODO
        # self.projectmenu.add_command(label='Open project TODO', command=open_project)
        self.projectmenu.add_command(label='Save project as', command=self.save_project)
        self.projectmenu.add_separator()
        self.projectmenu.add_command(label='Quit', command=self.destroy)

        # plugins menu
        self.pluginsmenu = Tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Plugins', menu=self.pluginsmenu)

        # about menu
        self.helpmenu = Tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About', command=self.show_about_window)

        # add menu to window
        self.config(menu=self.menubar)

        ################ LEFT PANEL
        self.left_frame = Frame(self)
        self.left_frame_top = Frame(self.left_frame)
        self.scene_manager = ExtendedListbox(self.left_frame, width=250, unique_titles=True)
        self.scene_manager.bind('<1>', self.__on_select_scene, '+')
        self.add_scene_btn = Button(self.left_frame_top, text='+', width=20, command=self._add_scene_btn_handler)
        self.del_scene_btn = Button(self.left_frame_top, text='-', width=20, command=self._del_scene_btn_handler)
        Label(self.left_frame_top, text='Scenes').pack(anchor='nw', side='left')
        self.add_scene_btn.pack(side='right', anchor='ne', padx=1)
        self.del_scene_btn.pack(side='right', anchor='ne', padx=1)
        self.left_frame_top.pack(anchor='nw', padx=5, pady=5, fill='both')
        self.left_frame.pack(side='left', fill='y')

        self.scene_scroll = Scrollbar(self.left_frame, orient='vertical')
        self.scene_scroll.pack(side='left',fill='y', expand='yes')
        self.scene_manager.pack(expand='yes', fill='y', anchor='nw')
        self.scene_scroll.config(command=self.scene_manager.yview)
        self.scene_manager.config(yscrollcommand=self.scene_scroll.set)

        ################ RIGHT PANEL
        self.right_frame = Frame(self)
        self.right_frame_top = Frame(self.right_frame)
        self.assets_manager = ExtendedListbox(self.right_frame, width=250, unique_titles=True)
        Label(self.right_frame_top, text='Assets').pack(anchor='nw',
            side='left')
        self.right_frame_top.pack(anchor='nw', padx=5, pady=5, fill='both')

        self.add_sprite_btn = Button(self.right_frame_top, text='+', width=20, command=self._add_sprite_btn_handler)
        self.del_sprite_btn = Button(self.right_frame_top, text='-', width=20, command=self._del_sprite_btn_handler)
        self.add_sprite_btn.pack(side='right', anchor='ne', padx=1)
        self.del_sprite_btn.pack(side='right', anchor='ne', padx=1)
        self.assets_manager.pack(side='left', expand='yes', fill='y', anchor='nw')
        self.right_frame.pack(side='right', fill='y')

        self.assets_scroll = Scrollbar(self.right_frame, orient='vertical')
        self.assets_scroll.pack(fill='y', expand='yes')
        self.assets_scroll.config(command=self.assets_manager.yview)
        self.assets_manager.config(yscrollcommand=self.assets_scroll.set)

        ################ RIGHT PANEL
        self.canvas_frame = Frame(self)
        self.canvas_frame.pack(expand='yes')

        ############################
        center(self)
        self.bind('<Delete>', self.__delete_sprite, '+')
        self.bind('<Up>', self.__up_key, '+')
        self.bind('<Down>', self.__down_key, '+')
        self.bind('<Right>', self.__right_key, '+')
        self.bind('<Left>', self.__left_key, '+')
        self.focus_force()

        self.__load_plugins()

    def __load_plugins(self):
        '''
        the "plugin system" is very simple:
        exist a file named '.plugins' where each line
        is a name of a python module. Each module is imported
        in start of phaser ide. The module must have 3 things:
        1. a attribute named 'title' (this name will be putted in
        menu)
        2. a method 'init', called after import
        3. a method 'execute' called in the click of menu
        '''
        a = open('./.plugins')
        modules = a.readlines()
        a.close()
        for i in modules:
            mod = importlib.import_module(i.replace('\n', ''))
            mod.init(self)
            self.pluginsmenu.add_command(label=mod.title,
                command=lambda:mod.execute(self))

    def project_is_loaded(self):
        '''
        returns true if project is loaded, else
        shows a message and returns false
        '''
        if self.current_project:
            return True
        MessageBox.warning(parent=self, title='No project found', message='No project found')
        return False

    def cur_canvas(self):
        '''
        returns the actual canvas instance shown in the screen
        '''
        return self.canvases.get(self.actual_canvas, None)

    def __reset_all_canvas(self):
        '''
        remove from screen all canvas
        '''
        for i in self.canvases:
            self.canvases[i].pack_forget()
        self.canvases = {}
        self.sprite_canvases = {}
        self.actual_canvas = None

    ################ SCENES
    def __on_select_scene(self, event):
        '''
        called when the user clicks in a scene
        in scene manager
        '''
        selection = self.scene_manager.get_selected()
        if selection:
            scene_name = selection.title
            if (scene_name != self.actual_canvas and self.actual_canvas != None) or self.actual_canvas == None:
                if self.actual_canvas:
                    self.canvases[self.actual_canvas].pack_forget()
                self.actual_canvas = scene_name
                self.cur_canvas().pack()

    def _add_scene_btn_handler(self):
        '''
        called when user clicks over add_scene_button
        '''
        if not self.project_is_loaded():
            return

        asw = AddSceneWindow(self, title='Add Scene')
        if asw.output:
            try:
                self.scene_manager.add_item(asw.output['name'], 'scene', 'icons/folder.png')
                ca = ExtendedCanvas(self.canvas_frame,
                    width=self.current_project.width,
                    height=self.current_project.height,
                    bg=self.current_project.bgcolor)
                ca.pack(anchor='sw', side='left')
                self.canvases[asw.output['name']] = ca
                # the list of sprites of this scene is a empty list
                self.sprite_canvases[asw.output['name']] = []
                if self.actual_canvas:
                    self.cur_canvas().pack_forget()
                self.actual_canvas = asw.output['name']
                # put focus in actual canvas
                self.scene_manager.desselect_all()
                self.scene_manager.select_last()
            except DuplicatedExtendedListboxItemException:
                MessageBox.warning(
                    parent=self,
                    title='DuplicatedExtendedListboxItemException',
                    message='a scene in project already contains this name')

    def _del_scene_btn_handler(self):
        '''
        called when user clicks over del_scene_button
        '''
        if not self.project_is_loaded():
            return

        selection = self.scene_manager.get_selected()
        if selection:
            scene_name = selection.title
            if OkCancel(self,
                'The scene *%s* will be delete. Are you sure?' % (scene_name),
                title='Are you sure?').output:

                self.scene_manager.remove_by_title(scene_name)
                self.canvases[scene_name].pack_forget()
                del self.canvases[scene_name]
                self.actual_canvas = None

    ################ ASSETS
    SUPPORTED_IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif', 'tiff']
    SUPPORTED_SOUND_FILES = ['mp3', 'ogg', 'wav']
    def get_file_name(self):
        '''
        opens a file dialog for file selection and returns
        the path
        '''
        image_ext = '.' + ' .'.join(PhaserEditor.SUPPORTED_IMAGE_TYPES)
        sound_ext = '.' + ' .'.join(PhaserEditor.SUPPORTED_SOUND_FILES)
        file_opt = dict(filetypes=[('Image Files', image_ext), ('Sound Files', sound_ext)])
        return tkFileDialog.askopenfilename(parent=self, **file_opt)

    def _add_sprite_btn_handler(self):
        '''
        called when user clicks over add_sprite_btn
        '''
        if not self.project_is_loaded():
            return

        file_name = self.get_file_name()
        if not file_name:
            return
        ext = posixpath.basename(file_name).split('.')[-1].lower()
        if file_name:
            if ext in PhaserEditor.SUPPORTED_SOUND_FILES:
                self.__add_sound_asset(file_name)
            elif ext in PhaserEditor.SUPPORTED_IMAGE_TYPES:
                self.__add_image_asset(file_name)

    def __add_sound_asset(self, file_name):
        '''
        called after select a music file
        '''
        asaw = AddSoundAssetWindow(self, path=file_name)
        if asaw.output:
            try:
                self.assets_manager.add_item(asaw.output['name'],
                    'sound', 'icons/headphone.png')
            except DuplicatedExtendedListboxItemException:
                MessageBox.warning(
                    parent=self,
                    title='DuplicatedExtendedListboxItemException',
                    message='a asset in project already contains this name')

    def __add_image_asset(self, file_name):
        '''
        called after select a image file
        '''
        aiaw = AddImageAssetWindow(self, path=file_name)
        if aiaw.output:
            try:
                item = self.assets_manager.add_item(aiaw.output['name'],
                    'image', 'icons/image.png')
                item.details = aiaw.output
                item.bind('<Double-Button-1>', self.__dbl_click_image_sprite, '+')
            except DuplicatedExtendedListboxItemException:
                MessageBox.warning(
                    parent=self,
                    title='DuplicatedExtendedListboxItemException',
                    message='a asset in project already contains this name')

    def _del_sprite_btn_handler(self):
        '''
        called when user clicks over del_sprite_btn
        '''
        if not self.project_is_loaded():
            return

        selection = self.assets_manager.get_selected()
        if selection:
            if OkCancel(self,
                'The asset *%s* will be delete and with him all yours sprites too. Are you sure?' % (selection.title),
                title='Are you sure?').output:
                self.assets_manager.remove_by_title(selection.title)
                self.remove_asset_by_name(selection.title)

    def __dbl_click_image_sprite(self, evt):
        '''
        called when user double clicks in the sprite image button
        '''
        if not self.actual_canvas:
            MessageBox.warning(
                    parent=self,
                    title='No scene specified',
                    message='Select/create a scene to put sprite')
            return
        canvas = self.cur_canvas()
        cx, cy = canvas.center
        # details is not defined in ExtendedListboxItem, but its created
        # in run time when you create a assets
        asset = self.assets_manager.get_selected().details
        component = None
        if asset['type'] == 'image':
            component = comp.ImageComponent(canvas, cx, cy, asset['path'],
                self, asset['name'])
        elif asset['type'] == 'sprite':
            # args order: canvas, x, y, path, ide, name, sprite_width, sprite_height
            component = comp.SpriteComponent(canvas, cx, cy, asset['path'],
                self, asset['name'], asset['sprite_width'],
                asset['sprite_height'], asset['autoplay'], asset['framerate'])
        if component:
            self.__add_sprite_to_canvas( component )

    def __add_sprite_to_canvas(self, sprite):
        '''
        called when the user double clicks in a assets in assets manager
        '''
        self.sprite_canvases[self.actual_canvas].append( sprite )
        sprite.bind('<1>', lambda evt: self.__select_sprite(sprite), '+')

    def desselect_all_sprites(self):
        for i in self.sprite_canvases[self.actual_canvas]:
            i.selected = False
            # if has rectangle bounds
            if i.bounds:
                i.bounds.style['outline'] = DRAG_CONTROL_STYLE['fill']
            i.bounds.update()
            i.update()

    def __select_sprite(self, sprite):
        '''
        called when the user clicks in a sprite
        '''
        self.desselect_all_sprites()
        sprite.selected = True
        sprite.bounds.style['outline'] = 'red'
        sprite.bounds.update()
        sprite.update()

    def get_selected_sprite(self):
        '''
        returns the selected sprite
        '''
        for i in self.sprite_canvases[self.actual_canvas]:
            if hasattr(i, 'selected') and i.selected:
                return i
        return None

    def __delete_sprite(self, evt):
        '''
        called when user clicks 'del' key
        '''
        selected = self.get_selected_sprite()
        if selected:
            self.sprite_canvases[self.actual_canvas].remove(selected)
            selected.bounds.delete()
            selected.lower_right.delete()
            selected.delete()

    def __right_key(self, evt):
        '''
        called when user clicks 'up' key
        '''
        selected = self.get_selected_sprite()
        if selected:
            selected.x += 1

    def __left_key(self, evt):
        '''
        called when user clicks 'up' key
        '''
        selected = self.get_selected_sprite()
        if selected:
            selected.x -= 1

    def __up_key(self, evt):
        '''
        called when user clicks 'up' key
        '''
        selected = self.get_selected_sprite()
        if selected:
            selected.y -= 1

    def __down_key(self, evt):
        '''
        called when user clicks 'up' key
        '''
        selected = self.get_selected_sprite()
        if selected:
            selected.y += 1

    def remove_asset_by_name(self, name):
        sprites_to_delete = {}
        for item in self.scene_manager.get_all():
            scene_name = item.title
            if not sprites_to_delete.has_key(scene_name):
                sprites_to_delete[scene_name] = []
            for sprite in self.sprite_canvases[scene_name]:
                if sprite.assetname == name:
                    sprites_to_delete[scene_name].append(sprite)
        for item in self.scene_manager.get_all():
            scene_name = item.title
            for i in sprites_to_delete[scene_name]:
                self.sprite_canvases[scene_name].remove(i)
                i.delete()

    ################### Menu events
    def show_about_window(self):
        AboutWindow(self)

    def save_project(self):
        if not self.current_project:
            return
        fn = tkFileDialog.asksaveasfilename()
        if fn:
            f = open(fn, 'w')
            f.write(self.current_project.get_json())
            f.close()

    def new_project(self):
        npw = NewProjectWindow(self)
        if npw.output:
            self.current_project = core.PhaserProject()
            self.current_project.fill_from_dict(npw.output)
            # clearing the scene/assets listbox
            self.scene_manager.delete_all()
            self.assets_manager.delete_all()
            self.title('Phaser - %s' % (npw.output['name']))

            # clearing the canvases
            self.__reset_all_canvas()

if __name__ == '__main__':
    top = PhaserEditor()
    # AboutWindow(top)
    top.mainloop()
