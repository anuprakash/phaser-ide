# logic editor
import boring.dialog
import boring.widgets
import boring.drawwidgets
from boring import *
import sensors
import controllers
import actuators


class LogicEditor(boring.dialog.DefaultDialog):
    def body(self, master):
        self.add_menu({
            'Sensors': [
                {
                    'title': 'Once on startup',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_ONCE),
                    'shortcut': 'Control+O'
                },
                {
                    'title': 'Always',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_ALWAYS),
                    'shortcut': 'Control+A'
                },
                {
                    'title': 'Keyboard',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_KEYBOARD),
                    'shortcut': 'Control+K'
                },
                {
                    'title': 'Joystick',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_JOYSTICK),
                    'shortcut': 'Control+K'
                },
                {
                    'title': 'Mouse',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_MOUSE),
                    'shortcut': 'Control+M'
                },
                {
                    'title': 'Message',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_MESSAGE),
                    'shortcut': 'Control+E'
                },
                {
                    'title': 'Property',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_PROPERTY),
                    'shortcut': 'Control+P'
                },
                {
                    'title': 'Collision',
                    'command': lambda : self.__add_sensor(sensors.SENSOR_COLLISION),
                    'shortcut': 'Control+C'
                }
            ],
            'Controlers': [
                {
                    'title': 'AND',
                    'command': lambda : self.__add_controller(constrollers.CONTROLLER_AND),
                    'shortcut': 'Control-F'
                },
                {
                    'title': 'OR',
                    'command': lambda : self.__add_controller(constrollers.CONTROLLER_OR),
                    'shortcut': 'Control-G'
                }
            ],
            'Actuators': [
                {
                    'title': 'Code',
                    'command': lambda : self.__add_actuator(actuators.ACTUATOR_CODE)
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
        if sensor_type == sensors.SENSOR_MESSAGE:
            mdw = sensors.MessageSensorDrawWindow(
                self.canvas
            )
            mdw.center()

    def __add_controller(self, controller_type):
        pass

    def __add_actuator(self, controller_type):
        pass