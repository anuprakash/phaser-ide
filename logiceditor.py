# logic editor
import boring.dialog
import boring.widgets
import boring.drawwidgets
from boring import *

SENSOR_ONCE = 0
SENSOR_ALWAYS = 1
SENSOR_KEYBOARD = 2
SENSOR_JOYSTICK = 3
SENSOR_MOUSE = 4 # TODO: permitir selecionar o objeto
SENSOR_MESSAGE = 5
SENSOR_PROPERTY = 6
SENSOR_COLLISION = 7

CONTROLLER_AND = 0
CONTROLLER_OR = 1

ACTUATOR_CODE = 0

class MessageSensorDrawWindow(boring.drawwidgets.DrawWindow):
    pass

class LogicEditor(boring.dialog.DefaultDialog):
    def body(self, master):
        self.add_menu({
            'Sensors': [
                {
                    'title': 'Once on startup',
                    'command': lambda : self.__add_sensor(SENSOR_ONCE),
                    'shortcut': 'Control+O'
                },
                {
                    'title': 'Always',
                    'command': lambda : self.__add_sensor(SENSOR_ALWAYS),
                    'shortcut': 'Control+A'
                },
                {
                    'title': 'Keyboard',
                    'command': lambda : self.__add_sensor(SENSOR_KEYBOARD),
                    'shortcut': 'Control+K'
                },
                {
                    'title': 'Joystick',
                    'command': lambda : self.__add_sensor(SENSOR_JOYSTICK),
                    'shortcut': 'Control+K'
                },
                {
                    'title': 'Mouse',
                    'command': lambda : self.__add_sensor(SENSOR_MOUSE),
                    'shortcut': 'Control+M'
                },
                {
                    'title': 'Message',
                    'command': lambda : self.__add_sensor(SENSOR_MESSAGE),
                    'shortcut': 'Control+E'
                },
                {
                    'title': 'Property',
                    'command': lambda : self.__add_sensor(SENSOR_PROPERTY),
                    'shortcut': 'Control+P'
                },
                {
                    'title': 'Collision',
                    'command': lambda : self.__add_sensor(SENSOR_COLLISION),
                    'shortcut': 'Control+C'
                }
            ],
            'Controlers': [
                {
                    'title': 'AND',
                    'command': lambda : self.__add_controller(CONTROLLER_AND),
                    'shortcut': 'Control-F'
                },
                {
                    'title': 'OR',
                    'command': lambda : self.__add_controller(CONTROLLER_OR),
                    'shortcut': 'Control-G'
                }
            ],
            'Actuators': [
                {
                    'title': 'Code',
                    'command': lambda : self.__add_actuator(ACTUATOR_CODE)
                }
            ]
        })

        self.canvas = boring.widgets.ExtendedCanvas(
            master,
            relief='flat',
            bd=0,
            highlightthickness=0,
            bg='#ededed'
        )
        self.canvas.pack(
            expand='yes', fill='both'
        )

        self.resizable(1, 1)
        # TODO: meximize in Windows
        self.attributes('-zoomed', 1)
        return self.canvas

    def __add_sensor(self, sensor_type):
        if sensor_type == SENSOR_MESSAGE:
            mdw = MessageSensorDrawWindow(
                self.canvas
            )
            mdw.center()

    def __add_controller(self, controller_type):
        pass

    def __add_actuator(self, controller_type):
        pass