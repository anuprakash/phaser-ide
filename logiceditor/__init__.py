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
        self.add_menu([
            [
                'Logic Editor', [
                    {
                        'title': 'Quit',
                        'command': self.destroy
                    }
                ]
            ],
            ['Sensors', [
                {
                    'title': 'Single Signal',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_SIGNAL),
                    'shortcut': 'Control-s'
                },
                {
                    'title': 'Always',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_ALWAYS),
                    'shortcut': 'Control-a'
                },
                {
                    'title': 'Keyboard',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_KEYBOARD),
                    'shortcut': 'Control-k'
                },
                {
                    'title': 'Joystick',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_JOYSTICK),
                    'shortcut': 'Control-j'
                },
                {
                    'title': 'Mouse',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_MOUSE),
                    'shortcut': 'Control-m'
                },
                {
                    'title': 'Message',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_MESSAGE),
                    'shortcut': 'Control-e'
                },
                {
                    'title': 'Property',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_PROPERTY),
                    'shortcut': 'Control-p'
                },
                {
                    'title': 'Collision',
                    'command': lambda *args : self.__add_sensor(sensors.SENSOR_COLLISION),
                    'shortcut': 'Control-c'
                }
            ]],
            ['Controlers', [
                {
                    'title': 'AND',
                    'command': lambda *args : self.__add_controller(controllers.CONTROLLER_AND),
                    'shortcut': 'Control-f'
                },
                {
                    'title': 'OR',
                    'command': lambda *args : self.__add_controller(controllers.CONTROLLER_OR),
                    'shortcut': 'Control-g'
                }
            ]],
            ['Actuators', [
                {
                    'title': 'Code',
                    'command': lambda *args : self.__add_actuator(actuators.ACTUATOR_CODE)
                },
                {
                    'title': 'Scene',
                    'command': lambda *args : self.__add_actuator(actuators.ACTUATOR_SCENE)
                },
                {
                    'title': 'Game',
                    'command': lambda *args : self.__add_actuator(actuators.ACTUATOR_GAME)
                }
            ]]
        ])

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
        elif sensor_type == sensors.SENSOR_SIGNAL:
            ssdw = sensors.SignalSensorDrawWindow(
                self.canvas
            )
            ssdw.center()
        elif sensor_type == sensors.SENSOR_ALWAYS:
            asdw = sensors.AlwaysSensorDrawWindow(
                self.canvas
            )
            asdw.center()

    def __add_controller(self, controller_type):
        if controller_type == controllers.CONTROLLER_AND:
            acdw = controllers.ANDControllerDrawWindow(
                self.canvas
            )
            acdw.center()
        elif controller_type == controllers.CONTROLLER_OR:
            ocdw = controllers.ORControllerDrawWindow(
                self.canvas
            )
            ocdw.center()

    def __add_actuator(self, controller_type):
        pass