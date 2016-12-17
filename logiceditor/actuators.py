# logiceditor:actuators

import core
import boring.draw
import boring.form

ACTUATOR_QUIT_GAME = 0
ACTUATOR_RESTART_GAME = 1

ACTUATOR_RESTART_SCENE = 2
ACTUATOR_LOAD_SCENE = 3 # TODO

ACTUATOR_CODE = 4

ACTUATOR_MOUSE_VISIBILITY = 5

# ADD OBJECT: x, y, z
# END OBJECT
# MAYBE: ADD 2D FILTER
# MOTION: POSITION AND ROTATION
# PROPERTY (ASSIGN, ADD, COPY)
# TOGGLE (TRUE/FALSE)
# SOUND

class GenericActuatorDrawWindow(core.GenericLogicEditorDrawWindow):
    def __init__(self, canvas, title='Sensor', widget=None):
        self.__connector = boring.draw.OvalDraw(
            canvas,
            -10,
            -10,
            5,
            5
        )
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
                'Code@text',
                font=('TkDefaultFont', 6)
            )
        )

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