import core
import tkFileDialog
import Tkinter
from windows import *
import posixpath

class PhaserEditor(Tkinter.Tk):
    def __init__(self):
        self.current_project = None
        self.canvases = {}
        self.actual_canvas = None

        Tkinter.Tk.__init__(self)
        ttk.Style().theme_use('clam')
        self.title('Phaser')
        self['bg'] = BG_COLOR
        self.geometry('%dx%d' % (1200, 600))

        # parent of all menus
        self.menubar = Tkinter.Menu(self, relief=Tkinter.FLAT)
        # file menu
        self.projectmenu = Tkinter.Menu(self.menubar, tearoff=0, relief=Tkinter.FLAT)
        self.menubar.add_cascade(label="Project", menu=self.projectmenu)
        self.projectmenu.add_command(label="New project", command=self.new_project)
        # TODO
        # self.projectmenu.add_command(label="Open project TODO", command=open_project)
        self.projectmenu.add_command(label="Save project as", command=self.save_project)
        self.projectmenu.add_separator()
        self.projectmenu.add_command(label="Quit", command=self.destroy)

        # about menu
        self.helpmenu = Tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About", command=self.show_about_window)

        # add menu to window
        self.config(menu=self.menubar)

        ################ LEFT PANEL
        self.left_frame = Frame(self)
        self.left_frame_top = Frame(self.left_frame)
        self.scene_manager = ExtendedListbox(self.left_frame, width=250, bg='#d1d8e0')
        self.scene_manager.bind('<1>', self.__on_select_scene, '+')
        self.add_scene_btn = Button(self.left_frame_top, text='+', width=20, command=self._add_scene_btn_handler)
        self.del_scene_btn = Button(self.left_frame_top, text='-', width=20, command=self._del_scene_btn_handler)
        Label(self.left_frame_top, text='Scenes').pack(anchor='nw', side='left')
        self.add_scene_btn.pack(side='right', anchor='ne', padx=1)
        self.del_scene_btn.pack(side='right', anchor='ne', padx=1)
        self.left_frame_top.pack(anchor='nw', padx=5, pady=5, fill='both')
        self.scene_manager.pack(side='left', expand='yes', fill='y', anchor='nw')
        self.left_frame.pack(side='left', fill='y')

        ################ RIGHT PANEL
        self.right_frame = Frame(self)
        self.right_frame_top = Frame(self.right_frame)
        self.assets_manager = ExtendedListbox(self.right_frame, width=250)
        Label(self.right_frame_top, text='Assets').pack(anchor='nw',
            side='left')
        self.right_frame_top.pack(anchor='nw', padx=5, pady=5, fill='both')

        self.add_sprite_btn = Button(self.right_frame_top, text='+', width=20, command=self._add_sprite_btn_handler)
        self.del_sprite_btn = Button(self.right_frame_top, text='-', width=20, command=self._del_sprite_btn_handler)
        self.add_sprite_btn.pack(side='right', anchor='ne', padx=1)
        self.del_sprite_btn.pack(side='right', anchor='ne', padx=1)
        self.assets_manager.pack(side='left', expand='yes', fill='y', anchor='nw')
        self.right_frame.pack(side='right', fill='y')

        ################ RIGHT PANEL
        self.canvas_frame = Frame(self)
        self.canvas_frame.pack(expand='yes')

        ############################
        center(self)

    def project_is_loaded(self):
        '''
        returns true if project is loaded, else
        shows a message and returns false
        '''
        if self.current_project:
            return True
        MessageBox.warning(title='No project found', message='No project found')
        return False

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
                self.canvases[self.actual_canvas].pack()

    def _add_scene_btn_handler(self):
        '''
        called when user clicks over add_scene_button
        '''
        if not self.project_is_loaded():
            return

        asw = AddSceneWindow(self, title='Add Scene')
        if asw.output:
            try:
                self.current_project.add_scene_from_dict(asw.output)
                self.scene_manager.add_item(asw.output['name'], 'scene', 'icons/folder.png')
                ca = ExtendedCanvas(self.canvas_frame,
                    width=self.current_project.width,
                    height=self.current_project.height,
                    bg=self.current_project.bgcolor)
                ca.pack(anchor='sw', side='left')
                self.canvases[asw.output['name']] = ca
                ca.create_text(10,10,text=asw.output['name'])
                if self.actual_canvas:
                    self.canvases[self.actual_canvas].pack_forget()
                self.actual_canvas = asw.output['name']
                # put focus in actual canvas
                self.scene_manager.desselect_all()
                self.scene_manager.select_last()
            except core.DuplicatedSceneNameException:
                MessageBox.warning(
                    title='DuplicatedSceneNameException',
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
                'The scene %s will be delete. Are you sure?' % (scene_name),
                title='Are you sure?').output:

                self.current_project.remove_scene_from_name(scene_name)
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
        basename = posixpath.basename(file_name)
        ext = basename.split('.')[-1].lower()
        if file_name:
            if ext in PhaserEditor.SUPPORTED_SOUND_FILES:
                asaw = AddSoundAssetWindow(self, default_name=basename.split('.')[0].lower())
                if asaw.output:
                    self.assets_manager.add_item(asaw.output['name'],
                        'sound', 'icons/headphone.png')
            elif ext in PhaserEditor.SUPPORTED_IMAGE_TYPES:
                aiaw = AddImageAssetWindow(self, default_name=basename.split('.')[0].lower())
                if aiaw.output:
                    self.assets_manager.add_item(aiaw.output['name'],
                        'image', 'icons/image.png')

    def _del_sprite_btn_handler(self):
        '''
        called when user clicks over del_sprite_btn
        '''
        if not self.project_is_loaded():
            return

        selection = self.assets_manager.get_selected()
        if selection:
            if OkCancel(self,
                'The asset %s will be delete. Are you sure?' % (selection.title),
                title='Are you sure?').output:
                self.assets_manager.remove_by_title(selection.title)

    ################### Menu events
    def show_about_window(self):
        AboutWindow(self)

    def save_project(self):
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

if __name__ == '__main__':
    top = PhaserEditor()
    top.mainloop()