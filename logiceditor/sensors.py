# logiceditor:sensors
import boring.drawwidgets
import boring.draw
import boring.form
import boring.widgets
import core
import widgets

SENSOR_SIGNAL = 0
SENSOR_ALWAYS = 1
SENSOR_KEYBOARD = 2
SENSOR_JOYSTICK = 3
SENSOR_MOUSE = 4 # TODO: permitir selecionar o objeto
SENSOR_MESSAGE = 5
SENSOR_PROPERTY = 6 # TODO: permitir selecionar um objeto e a propriedade
    # Se o usuario quiser adicionar uma propriedade global ele deve criar um objeto empty
SENSOR_COLLISION = 7


class GenericSensorDrawWindow(core.GenericLogicEditorDrawWindow):
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
            fill='#aaa',
            radius=[3]*4,
            title=title,
            widget=widget,
            emissor=True,
            emissor_type='sensor',
            receptor=False
        )

class MessageSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, canvas):
        GenericSensorDrawWindow.__init__(
            self,
            canvas,
            title='Message',
            widget=boring.form.FormFrame(
                canvas,
                'Subject@string\nalways@check',
                font=('TkDefaultFont', 6)
            )
        )

class SignalSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, canvas):
        GenericSensorDrawWindow.__init__(
            self,
            canvas,
            title='Signal'
        )


class AlwaysSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, canvas):
        GenericSensorDrawWindow.__init__(
            self,
            canvas,
            title='Always'
        )

class KeyboardSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, canvas):
        widgets_list = dict(boring.form.DEFAULT_FORM_WIDGETS)
        widgets_list.update(
            keyboardkey=widgets.KeyboardSensorWidget
        )

        GenericSensorDrawWindow.__init__(
            self,
            canvas,
            title='Keyboard',
            widget=boring.form.FormFrame(
                canvas,
                'Tap@check\nkey@keyboardkey',
                font=('TkDefaultFont', 6),
                inputswidgets=widgets_list
            ),
        )