#!/usr/bin/env python
# coding: utf-8

import sys
import core
PYTHON_3 = sys.version_info.major == 3
if PYTHON_3:
    from tkinter import filedialog as tkFileDialog
    import tkinter
else:
    import tkFileDialog
    import Tkinter
from windows import *
from windows.shortcuts import *
import components as comp
import posixpath
import importlib
import json
import random
import string
import logiceditor
import boring
import boring.widgets
import windows.newproject
import windows.about
import windows.scene
import windows.assets
import boring.ttk as ttk

VErSIOn = 'alpha'

class PhaserEditor(boring.Window):
    def __init__(self):
        self.__current_project = None
        # stores the canvas itself
        # the key is the scene name
        self.canvases = {}
        # stores all sprite of each canvas
        # the key is the scene name
        self.sprite_canvases = {}
        self.actual_canvas = None

        Tkinter.Tk.__init__(self)
        ttk.Style().theme_use('clam')
        self['bg'] = boring.BG_COLOR
        self.geometry('%dx%d' % (1200, 600))

        # for drag loacking
        self.kmap = dict()
        self.__pressing_x = False
        self.__pressing_y = False
        self.bind('<Any-KeyPress>', self.__press_key, '+')
        self.bind('<Any-KeyRelease>', self.__release_key, '+')

        # parent of all menus
        self.menubar = Tkinter.Menu(
            self,
            relief=Tkinter.FLAT
        )
        ################################ file menu
        self.projectmenu = Tkinter.Menu(
            self.menubar,
            tearoff=0,
            relief=Tkinter.FLAT
        )
        self.menubar.add_cascade(
            label='Project',
            menu=self.projectmenu,
            underline=0
        )
        self.projectmenu.add_command(
            label='New project',
            command=self.new_project,
            underline=0,
            accelerator='Control+N'
        )

        self.projectmenu.add_command(
            label='Open project from JSON',
            command=self.open_json_project,
            underline=0,
            accelerator='Control+O'
        )
        self.projectmenu.add_command(
            label='Save project as JSON',
            command=self.save_project_as_json,
            underline=1,
            accelerator='Control+S'
        )
        self.projectmenu.add_command(
            label='Project properties',
            command=self.show_project_properties,
            underline=1
        )
        self.projectmenu.add_separator()
        self.projectmenu.add_command(
            label='Quit',
            command=self.destroy,
            underline=0
        )

        self.bind('<Control-n>', lambda e: self.new_project(), '+')
        self.bind('<Control-m>', lambda e: self._add_scene_btn_handler(), '+')
        self.bind('<Control-x>', lambda e: self._add_sprite_btn_handler(), '+')
        self.bind('<Control-s>', lambda e: self.save_project_as_json(), '+')
        self.bind('<Control-o>', lambda e: self.open_json_project(), '+')
        self.bind('<Alt-p>', lambda e: self.show_project_properties(), '+')
        ################################ view menu
        self.viewmenu = Tkinter.Menu(
            self.menubar,
            tearoff=0,
            relief=Tkinter.FLAT
        )
        self.menubar.add_cascade(
            label='View',
            menu=self.viewmenu,
            underline=0
        )
        self.viewmenu.add_command(
            label='Logic Editor',
            command=self.show_logic_editor,
            underline=0
        )
        ################################ plugins menu
        self.pluginsmenu = Tkinter.Menu(
            self.menubar,
            tearoff=0
        )
        self.menubar.add_cascade(
            label='Plugins',
            menu=self.pluginsmenu,
            underline=1
        )
        ################################ about menu
        self.helpmenu = Tkinter.Menu(
            self.menubar,
            tearoff=0
        )
        self.menubar.add_cascade(
            label='Help',
            menu=self.helpmenu,
            underline=0
        )
        self.helpmenu.add_command(
            label='Shortcuts',
            command=self.show_shortcuts_window
        )
        self.helpmenu.add_command(
            label='About',
            command=self.show_about_window
        )

        # add menu to window
        self.config(menu=self.menubar)

        self.left_panel = boring.widgets.Frame(self)
        self.left_panel.pack(
            fill='y',
            side='left'
        )

        ################ LEFT PANEL
        self.left_frame = boring.widgets.Frame(self.left_panel)
        self.left_frame_top = boring.widgets.Frame(self.left_frame)
        self.scene_manager = boring.widgets.ExtendedListbox(
            self.left_frame,
            width=250,
            unique_titles=True
        )
        self.scene_manager.bind('<1>', self.__on_select_scene, '+')
        self.add_scene_btn = boring.widgets.Button(
            self.left_frame_top,
            text='+',
            width=20,
            command=self._add_scene_btn_handler
        )
        self.del_scene_btn = boring.widgets.Button(
            self.left_frame_top,
            text='-',
            width=20,
            command=self._del_scene_btn_handler
        )
        boring.widgets.Label(self.left_frame_top, text='Scenes').pack(
            anchor='nw',
            side='left'
        )
        self.add_scene_btn.pack(
            side='right',
            anchor='ne',
            padx=1
        )
        self.del_scene_btn.pack(
            side='right',
            anchor='ne',
            padx=1
        )
        self.left_frame_top.pack(
            anchor='nw',
            padx=5,
            pady=5,
            fill='both'
        )
        self.left_frame.pack(
            fill='y',
            expand='yes'
        )

        self.scene_scroll = boring.widgets.Scrollbar(self.left_frame, orient='vertical')

        self.scene_manager.pack(
            side='left',
            expand='yes',
            fill='y',
            anchor='nw'
        )
        self.scene_scroll.pack(
            fill='y',
            expand='yes'
        )
        self.scene_scroll.config(command=self.scene_manager.yview)
        self.scene_manager.config(yscrollcommand=self.scene_scroll.set)

        ################ RIGHT PANEL
        self.right_frame = boring.widgets.Frame(self.left_panel)
        self.right_frame_top = boring.widgets.Frame(self.right_frame)
        self.assets_manager = boring.widgets.ExtendedListbox(
            self.right_frame,
            width=250,
            unique_titles=True
        )
        boring.widgets.Label(self.right_frame_top, text='Assets').pack(
            anchor='nw',
            side='left'
        )
        self.right_frame_top.pack(
            anchor='nw',
            padx=5,
            pady=5,
            fill='both'
        )

        self.add_sprite_btn = boring.widgets.Button(
            self.right_frame_top,
            text='+', width=20,
            command=self._add_sprite_btn_handler
        )
        self.del_sprite_btn = boring.widgets.Button(
            self.right_frame_top,
            text='-',
            width=20,
            command=self._del_sprite_btn_handler
        )
        self.add_sprite_btn.pack(
            side='right',
            anchor='ne',
            padx=1)
        self.del_sprite_btn.pack(
            side='right',
            anchor='ne',
            padx=1
        )
        self.assets_manager.pack(
            side='left',
            expand='yes',
            fill='y',
            anchor='nw'
        )
        self.right_frame.pack(
            fill='y',
            expand='yes'
        )

        self.assets_scroll = boring.widgets.Scrollbar(
            self.right_frame,
            orient='vertical'
        )
        self.assets_scroll.pack(
            fill='y',
            expand='yes'
        )
        self.assets_scroll.config(command=self.assets_manager.yview)
        self.assets_manager.config(yscrollcommand=self.assets_scroll.set)

        ################ RIGHT PANEL
        self.canvas_frame = boring.widgets.Frame(self)
        self.canvas_frame.pack(
            expand='yes'
        )

        ############################
        self.center()
        self.bind('<Delete>', self.__delete_sprite, '+')
        self.bind('<Up>', self.__up_key, '+')
        self.bind('<Down>', self.__down_key, '+')
        self.bind('<Right>', self.__right_key, '+')
        self.bind('<Left>', self.__left_key, '+')
        self.focus_force()

        self.__load_plugins()
        self.set_title()

    def __release_key(self, event):
        '''
        called when you release any key (keyboard)
        '''
        self.kmap[event.keysym] = False

    def __press_key(self, event):
        '''
        called when you release any key (keyboard)
        '''
        self.kmap[event.keysym] = True

    @property
    def current_project(self):
        return self.__current_project

    @current_project.setter
    def current_project(self, value):
        self.__current_project = value
        self.set_title()

    def set_title(self):
        self.title('Phaser - %s - version: %s' % ('No project loaded' if not self.current_project else self.current_project.name, VErSIOn))

    def save_project_as_json(self):
        '''
        called when you press ctrl + s
        '''
        if self.current_project:
            json_dict = self.current_project.get_dict()
            json_dict.update(
                scenes=self.get_scenes_dict(),
                assets=self.get_assets_dict()
            )
            filename = tkFileDialog.asksaveasfilename()
            if filename:
                f = open(filename, 'w')
                f.write( json.dumps(json_dict) )
                f.close()
                boring.dialog.MessageBox.info(
                    parent=self, title='Success',
                    message='Project saved!'
                )

    def __gen_sprite_name(self):
        '''
        generates a random name
        '''
        return ''.join( [random.choice(string.letters) for i in xrange(15)] )

    def __get_file_content(self, file_path): # TODO: utils
        '''
        returns the content of file
        '''
        fs = open(file_path)
        content = fs.read()
        fs.close()
        return content

    def open_json_project(self):
        '''
        called when you press ctrl + o
        '''
        if self.current_project and (not boring.dialog.OkCancel(self, 'A loaded project already exists. Do you wish to continue?').output):
            return
        self.__reset_ide()

        file_opt = dict(filetypes=[('JSON Project', '.json')])
        file_name = tkFileDialog.askopenfilename(parent=self, **file_opt)
        if file_name:
            try:
                json_project = json.loads( self.__get_file_content(file_name) )
                self.current_project = core.PhaserProject(json_project)
                # the assets must be loaded first
                # because the scene loading will try get assets information
                # to put the sprite in ide
                self.load_assets_from_dictlist( json_project['assets'] )
                self.load_scenes_from_dictlist( json_project['scenes'] )
            except Exception, e:
                boring.dialog.MessageBox.warning(
                    parent=self,
                    title='Error loading JSON project',
                    message='The JSON format is wrong'
                )
                raise e

    def load_scenes_from_dictlist(self, _list):
        '''
        fill the ide with scenes in '_list'
        '''
        for scene in _list:
            self.add_scene( scene['name'] )
            for sprite in scene['sprites']:
                component = self.add_sprite(
                    scene['name'], sprite
                )

    def load_assets_from_dictlist(self, _list):
        '''
        fill the ide with assets in '_list'
        '''
        for asset in _list:
            self.add_asset( asset )

    def get_assets_dict(self):
        '''
        returns a list where each item is a dict describing
        the asset.
        used when you save the project
        '''
        result = []
        for asset in self.assets_manager.get_all():
            result.append( asset.details )
        return result

    def get_scenes_dict(self):
        '''
        returns a list where each item is a dict describing
        the scene.
        used when you save the project
        '''
        result = []
        for scenename in self.sprite_canvases.keys():
            d = {}
            result.append({
                'name': scenename,
                'sprites': self.get_sprites_dict(self.sprite_canvases[scenename])
            })
        return result

    def get_sprites_dict(self, sprites):
        '''
        sprites: a list of sprites
        this function receive a list of components
        and transforms them in a list where each item
        is a dict describind it
        '''
        result = []
        for sprite in sprites:
            if type(sprite) == comp.ImageComponent:
                result.append({
                    'name': sprite.name,
                    'assetname': sprite.assetname,
                    'x': sprite.x,
                    'y': sprite.y
                })
            elif type(sprite) == comp.SpriteComponent:
                result.append({
                    'name': sprite.name,
                    'assetname': sprite.assetname,
                    'x': sprite.x,
                    'y': sprite.y,
                    'framerate': sprite.framerate,
                    'autoplay': sprite.autoplay
                })
        return result

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
            self.pluginsmenu.add_command(
                label=mod.title,
                command=lambda:mod.execute(self)
            )

    def update_canvases(self):
        '''
        updates the bg, width and height of all canvases
        '''
        for canvas in self.canvases.values():
            canvas['bg'] = self.current_project.bgcolor
            canvas['width'] = self.current_project.width
            canvas['height'] = self.current_project.height

    def project_is_loaded(self):
        '''
        returns true if project is loaded, else
        shows a message and returns false
        '''
        if self.current_project:
            return True
        boring.dialog.MessageBox.warning(
            parent=self,
            title='No project found',
            message='No project found'
        )
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

    ################ VIEW MENU
    def show_logic_editor(self):
        '''
        called when the user clicks in View > Show logic editor
        '''
        logiceditor.LogicEditor(self)

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

        asw = windows.scene.AddSceneWindow(self)
        if asw.output:
            try:
                self.add_scene(asw.output['name'])
            except boring.widgets.DuplicatedExtendedListboxItemException:
                boring.dialog.MessageBox.warning(
                    parent=self,
                    title='DuplicatedExtendedListboxItemException',
                    message='a scene in project already contains this name')

    def add_scene(self, name):
        '''
        add an icon in scene manager and fills the canvas
        '''
        self.scene_manager.add_item(name, 'scene', 'icons/folder.png')
        ca = boring.widgets.ExtendedCanvas(self.canvas_frame,
            width=self.current_project.width,
            height=self.current_project.height,
            bg=self.current_project.bgcolor)
        ca.pack(anchor='sw', side='left')
        self.canvases[name] = ca
        # the list of sprites of this scene is a empty list
        self.sprite_canvases[name] = []
        if self.actual_canvas:
            self.cur_canvas().pack_forget()
        self.actual_canvas = name
        # put focus in actual canvas
        self.scene_manager.desselect_all()
        self.scene_manager.select_last()

    def _del_scene_btn_handler(self):
        '''
        called when user clicks over del_scene_button
        '''
        if not self.project_is_loaded():
            return

        selection = self.scene_manager.get_selected()
        if selection:
            scene_name = selection.title
            if boring.dialog.OkCancel(self,
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
                boring.diloag.MessageBox.warning(
                    parent=self,
                    title='DuplicatedExtendedListboxItemException',
                    message='a asset in project already contains this name')

    def __add_image_asset(self, file_name):
        '''
        called after select a image file
        '''
        aiaw = windows.assets.AddImageAssetWindow(self, path=file_name)
        if aiaw.output:
            try:
                self.add_asset( aiaw.output )
            except DuplicatedExtendedListboxItemException:
                boring.diloag.MessageBox.warning(
                    parent=self,
                    title='DuplicatedExtendedListboxItemException',
                    message='a asset in project already contains this name')

    def add_asset(self, details):
        '''
        add a asset in IDE
        details must be a dict describeing the asset
        can raises a DuplicatedExtendedListboxItemException
        use in loading json project
        '''
        if details['type'] in ('image', 'sprite'):
            item = self.assets_manager.add_item(details['name'],
                'image', 'icons/image.png')
            item.bind('<Double-Button-1>', lambda event : self.__dbl_click_image_asset(item), '+')
        item.details = details

    def _del_sprite_btn_handler(self):
        '''
        called when user clicks over del_sprite_btn
        '''
        if not self.project_is_loaded():
            return

        selection = self.assets_manager.get_selected()
        if selection:
            if boring.dialog.OkCancel(self,
                'The asset *%s* will be delete and with him all yours sprites too. Are you sure?' % (selection.title),
                title='Are you sure?').output:
                self.assets_manager.remove_by_title(selection.title)
                self.remove_asset_by_name(selection.title)

    def add_sprite(self, scenename, _dict):
        '''
        puts in canvas of scene named 'scenename' a component

        return the sprite
        '''
        asset = self.get_asset_details_by_name( _dict['assetname'] )

        kws = dict(**_dict)

        kws.update(
            canvas = self.canvases[scenename],
            path = asset['path'],
            ide = self
        )
        
        sprite = None

        if asset['type'] == 'image':
            sprite = comp.ImageComponent( **kws )
        elif asset['type'] == 'sprite':
            kws.update(
                sprite_width = asset['sprite_width'],
                sprite_height = asset['sprite_height']
            )
            sprite = comp.SpriteComponent( **kws )
        # binds common events
        if sprite:
            sprite.details = _dict
            self.__add_sprite_to_canvas( sprite )
        return sprite

    def __dbl_click_image_asset(self, item):
        '''
        called when user double clicks in the asset image button
        '''
        if not self.actual_canvas:
            boring.dialog.MessageBox.warning(
                    parent=self,
                    title='No scene specified',
                    message='Select/create a scene to put sprite')
            return

        cx, cy = self.cur_canvas().center
        # scenename, _dict
        kws = dict(
            name = self.__gen_sprite_name(),
            x = cx, y = cy,
            path = item.details['path'],
            assetname = item.title
        )
        if item.details['type'] == 'sprite':
            kws.update(
                sprite_width = item.details['sprite_width'],
                sprite_height = item.details['sprite_height'],
                framerate = 10,
                autoplay = True
            )
        self.add_sprite(
            self.actual_canvas, # the actual_canvas field is the name of scene
            kws
        )

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
                i.bounds.style['outline'] = boring.drag.DRAG_CONTROL_STYLE['fill']
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
        '''
        remove a asset and all 'childs' (sprites)
        '''
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

    def get_asset_details_by_name(self, name):
        '''
        returns the details of a asset gived your name
        '''
        for i in self.assets_manager.get_all():
            if i.details['name'] == name:
                return i.details
        return None

    ################### Menu events
    def show_shortcuts_window(self):
        '''
        called when you click Help > shortcuts
        '''
        ShortcutsWindow(self)

    def show_about_window(self):
        '''
        called when you click Help > About
        '''
        windows.about.AboutWindow(self)

    def new_project(self):
        if self.current_project and (not boring.dialog.OkCancel(self, 'A loaded project already exists. Do you wish to continue?').output):
            return
        npw = windows.newproject.NewProjectWindow(self)
        if npw.output:
            self.__reset_ide()
            self.current_project = core.PhaserProject(npw.output)

    def __reset_ide(self):
        '''
        clears all canvases, scenes, sprite etc...
        '''
        self.current_project = None
        self.scene_manager.delete_all()
        self.assets_manager.delete_all()
        self.__reset_all_canvas()

    def show_project_properties(self):
        '''
        called in Project > Project Properties
        '''
        if self.current_project:
            npw = windows.newproject.NewProjectWindow(self, _dict=self.current_project.get_dict())
            if npw.output:
                self.current_project = core.PhaserProject()
                self.current_project.fill_from_dict(npw.output)
                self.set_title()
                # if your change the bg color, or the size of project
                # all already created canvas must be updated
                self.update_canvases()

if __name__ == '__main__':
    top = PhaserEditor()
    top.focus_force()
    # AboutWindow(top)
    top.mainloop()
