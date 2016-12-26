# logiceditor:actuators

import core
import boring.draw
import boring.form
import boring.menus

ACTUATOR_QUIT_GAME = 0
ACTUATOR_RESTART_GAME = 1
ACTUATOR_RESTART_SCENE = 2
ACTUATOR_LOAD_SCENE = 3
ACTUATOR_CODE = 4
ACTUATOR_MOUSE_VISIBILITY = 5
ACTUATOR_LOAD_ASSETS = 6

# ADD OBJECT: x, y, z
# END OBJECT
# MAYBE: ADD 2D FILTER
# MOTION: POSITION AND ROTATION
# PROPERTY (ASSIGN, ADD, COPY)
# TOGGLE (TRUE/FALSE)
# SOUND

class GenericActuatorDrawWindow(core.GenericLogicEditorDrawWindow):
    def __init__(self, canvas, title='Sensor', widget=None):
        core.GenericLogicEditorDrawWindow.__init__(
            self,
            canvas,
            fill='#333',
            radius=[3]*4,
            title=title,
            widget=widget,
            emissor=False,
            receptor_type='actuator',
            receptor=True
        )

#### GAME
class QuitGameActuatorDrawWindow(GenericActuatorDrawWindow):
    def __init__(self, canvas):
        GenericActuatorDrawWindow.__init__(
            self,
            canvas,
            title='Quit Game'
        )

class RestartGameActuatorDrawWindow(GenericActuatorDrawWindow):
    def __init__(self, canvas):
        GenericActuatorDrawWindow.__init__(
            self,
            canvas,
            title='Restart Game'
        )

class RestartSceneActuatorDrawWindow(GenericActuatorDrawWindow):
    def __init__(self, canvas):
        GenericActuatorDrawWindow.__init__(
            self,
            canvas,
            title='Restart Scene'
        )

class CodeActuatorDrawWindow(GenericActuatorDrawWindow):
    def __init__(self, canvas):
        GenericActuatorDrawWindow.__init__(
            self,
            canvas,
            title='Code',
            widget=boring.form.FormFrame(
                canvas,
                'Script@text',
                font=('TkDefaultFont', 6)
            )
        )

    def set_code(self, code):
        self.widget.inputs[0].text = code

    @property
    def value(self):
        return self.widget.inputs[0].text

class MouseVisibilityActuatorDrawWindow(GenericActuatorDrawWindow):
    def __init__(self, canvas):
        GenericActuatorDrawWindow.__init__(
            self,
            canvas,
            title='Mouse',
            widget=boring.form.FormFrame(
                canvas,
                'Visible@check',
                font=('TkDefaultFont', 6)
            )
        )

class LoadAssetsActuatorDrawWindow(GenericActuatorDrawWindow):
    def __init__(self, canvas, get_assets_func=None):
        self.__get_assets_func = get_assets_func
        self.__stack = boring.widgets.RemovalButtonsStack(canvas)
        GenericActuatorDrawWindow.__init__(
            self,
            canvas,
            title='Load Assets',
            widget=self.__stack
        )
        self.__add_button = boring.draw.TextDraw(
            canvas, self.x+self.width - 5, self.y+(self.height/2), '+',
            anchor='e', fill='white'
        )
        self.__add_button.bind('<1>', self.__add_button_click, '+')

    def __add_button_click(self, event=None):
        if not self.__get_assets_func:
            return
        items = []
        for i in self.__get_assets_func():
            items.append({
                'name': i.get('name'),
                'subtitle': i.get('type'),
                'command': self.__gen_select_asset_function(i)
            })
        boring.menus.CommandChooserWindow.popup(items)

    def __gen_select_asset_function(self, item):
        def __final(*args):
            self.add_asset(item.get('name'))
        return __final

    def update(self):
        GenericActuatorDrawWindow.update(self)
        self.__add_button.xy = [
            self.x+self.width-5,
            self.y+(self.height/2)
        ]

    def add_asset(self, asset_name):
        try:
            self.__stack.add(asset_name)
        except boring.widgets.DuplicatedRemovalButtonException:
            pass

    @property
    def value(self):
        return self.__stack.value

class LoadSceneActuatorDrawWindow(GenericActuatorDrawWindow):
    def __init__(self, canvas, get_scene_func=None):
        self.__get_scene_func = get_scene_func
        self.__scenes_options = boring.menus.OptionMenu(
            canvas,
            get_items_func=self.__get_scenes
        )
        GenericActuatorDrawWindow.__init__(
            self,
            canvas,
            title='Load Scene',
            widget=self.__scenes_options
        )

    def __get_scenes(self, event=None):
        options = []
        if self.__get_scene_func:
            for i in self.__get_scene_func():
                options.append({
                    'name': i,
                    'subtitle': 'scene',
                    'icon': 'icons/folder.png'
                })
        return options

    @property
    def value(self):
        return self.__scenes_options.value

    @value.setter
    def value(self, value):
        self.__scenes_options.value = value