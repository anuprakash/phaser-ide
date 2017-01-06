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
SENSOR_PRELOAD = 8


class GenericSensorDrawWindow(core.GenericLogicEditorDrawWindow):
    def __init__(self, logiceditor, title='Sensor', widget=None):
        core.GenericLogicEditorDrawWindow.__init__(
            self,
            logiceditor,
            fill='#ddd',
            radius=[5,0,0,5],
            title=title,
            widget=widget,
            emissor=True,
            emissor_type='sensor',
            receptor=False,
            close_function=self.__remove_sensor
        )

    def __remove_sensor(self, event=None):
        self.logiceditor.sensors.remove(self)

class MessageSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, logiceditor):
        GenericSensorDrawWindow.__init__(
            self,
            logiceditor,
            title='Message',
            widget=boring.form.FormFrame(
                logiceditor.canvas,
                'Subject@string\nalways@check',
                font=('TkDefaultFont', 6)
            )
        )

    @property
    def subject(self):
        return self.widget.values[0]

    @property
    def always(self):
        return self.widget.values[1]

class SignalSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, logiceditor):
        GenericSensorDrawWindow.__init__(
            self,
            logiceditor,
            title='Signal'
        )


class AlwaysSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, logiceditor):
        GenericSensorDrawWindow.__init__(
            self,
            logiceditor,
            title='Always'
        )

class KeyboardSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, logiceditor):
        widgets_list = dict(boring.form.DEFAULT_FORM_WIDGETS)
        widgets_list.update(
            keyboardkey=widgets.KeyboardSensorWidget
        )

        GenericSensorDrawWindow.__init__(
            self,
            logiceditor,
            title='Keyboard',
            widget=boring.form.FormFrame(
                logiceditor,
                'Tap@check\nkey@keyboardkey',
                font=('TkDefaultFont', 6),
                inputswidgets=widgets_list
            ),
        )

class PreloadSensorDrawWindow(GenericSensorDrawWindow):
    def __init__(self, logiceditor):
        GenericSensorDrawWindow.__init__(
            self,
            logiceditor,
            title='Preload'
        )