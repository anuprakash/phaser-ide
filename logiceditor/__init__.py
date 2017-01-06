# logic editor

import boring.widgets
import boring.drawwidgets
import boring.menus
from boring import *
import sensors
import controllers
import actuators


class LogicEditor(SubWindow):
    def __init__(self, master):
        SubWindow.__init__(self, master)
        self.controllers = []
        self.sensors = []
        self.actuators = []

        self.canvas = boring.widgets.ExtendedCanvas(
            self,
            relief='flat',
            bd=0,
            highlightthickness=0,
            bg='#ededed',
            draggable=True
        )
        self.canvas.pack(
            expand='yes',
            fill='both'
        )

        self.__menu_items = [
            dict(
                name='Add single signal sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_SIGNAL)
            ),
            dict(
                name='Quit/close Logic Editor',
                command=lambda *args : self.withdraw()
            ),
            dict(
                name='Add Always sensor',
                command=lambda *args: self.__add_sensor(sensors.SENSOR_ALWAYS)
            ),
            dict(
                name='Add Keyboard sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_KEYBOARD)
            ),
            dict(
                name='Add Joystick sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_JOYSTICK)
            ),
            dict(
                name='Add Mouse sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_MOUSE)
            ),
            dict(
                name='Add Message sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_MESSAGE)
            ),
            dict(
                name='Add Property sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_PROPERTY)
            ),
            dict(
                name='Add Collision sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_COLLISION)
            ),
            dict(
                name='Add Preload sensor',
                command=lambda *args : self.__add_sensor(sensors.SENSOR_PRELOAD)
            ),
            dict(
                name='Add AND Controller',
                command=lambda *args : self.__add_controller(controllers.CONTROLLER_AND)
            ),
            dict(
                name='Add OR Controller',
                command=lambda *args : self.__add_controller(controllers.CONTROLLER_OR)
            ),
            dict(
                name='Add Quit Game Actuator',
                command=lambda *args : self.__add_actuator(actuators.ACTUATOR_QUIT_GAME)
            ),
            dict(
                name='Add Restart Game Actuator',
                command=lambda *args : self.__add_actuator(actuators.ACTUATOR_RESTART_GAME)
            ),
            dict(
                name='Add Restart Scene Actuator',
                command=lambda *args: self.__add_actuator(actuators.ACTUATOR_RESTART_SCENE)
            ),
            dict(
                name='Add Code Actuator',
                subtitle='Run a script',
                command=lambda *args : self.__add_actuator(actuators.ACTUATOR_CODE)
            ),
            dict(
                name='Add Mouse Visibility Actuator',
                subtitle='Turns on/off the visibility of mouse',
                command=lambda *args: self.__add_actuator(actuators.ACTUATOR_MOUSE_VISIBILITY)
            ),
            dict(
                name='Add Load Scene Actuator',
                subtitle='Loads a scene',
                command=lambda *args: self.__add_actuator(actuators.ACTUATOR_LOAD_SCENE)
            ),
            dict(
                name='Add Load Assets Actuator',
                subtitle='Loads many assets',
                command=lambda *args: self.__add_actuator(actuators.ACTUATOR_LOAD_ASSETS)
            ),

            dict(
                name='Clear Canvas Scroll',
                subtitle='Restore the real position of objects before your scrolling',
                command=self.__clear_canvas_scroll
            ),
        ]
        self.bind(
            '<Control-space>',
            lambda evt: boring.menus.CommandChooserWindow.popup(self.__menu_items),
            '+'
        )

        self.resizable(1, 1)
        # TODO: maximize in Windows
        self.attributes('-zoomed', 1)

        self.protocol('WM_DELETE_WINDOW', self.hide)

    def __clear_canvas_scroll(self, *args):
        self.canvas.clear_scroll()

    def __add_sensor(self, sensor_type):
        sensor = None
        if sensor_type == sensors.SENSOR_MESSAGE:
            sensor = sensors.MessageSensorDrawWindow(self)
        elif sensor_type == sensors.SENSOR_SIGNAL:
            sensor = sensors.SignalSensorDrawWindow(self)
        elif sensor_type == sensors.SENSOR_ALWAYS:
            sensor = sensors.AlwaysSensorDrawWindow(self)
        elif sensor_type == sensors.SENSOR_KEYBOARD:
            sensor = sensors.KeyboardSensorDrawWindow(self)
        elif sensor_type == sensors.SENSOR_PRELOAD:
            sensor = sensors.PreloadSensorDrawWindow(self)

        if sensor:
            self.sensors.append(sensor)
            sensor.center()

    def __add_controller(self, controller_type):
        controller = None
        if controller_type == controllers.CONTROLLER_AND:
            controller = controllers.ANDControllerDrawWindow(self)
        elif controller_type == controllers.CONTROLLER_OR:
            controller = controllers.ORControllerDrawWindow(self)

        if controller:
            self.controllers.append(controller)
            controller.center()

    def __add_actuator(self, actuator_type):
        actuator = None
        if actuator_type == actuators.ACTUATOR_QUIT_GAME:
            actuator = actuators.QuitGameActuatorDrawWindow(self)
        elif actuator_type == actuators.ACTUATOR_RESTART_GAME:
            actuator = actuators.RestartGameActuatorDrawWindow(self)
        elif actuator_type == actuators.ACTUATOR_RESTART_SCENE:
            actuator = actuators.RestartSceneActuatorDrawWindow(self)
        elif actuator_type == actuators.ACTUATOR_CODE:
            actuator = actuators.CodeActuatorDrawWindow(self.canvas)
        elif actuator_type == actuators.ACTUATOR_MOUSE_VISIBILITY:
            actuator = actuators.MouseVisibilityActuatorDrawWindow(self)
        elif actuator_type == actuators.ACTUATOR_LOAD_SCENE:
            actuator = actuators.LoadSceneActuatorDrawWindow(
                self, get_scene_func=self.__get_scene_list
            )
        elif actuator_type == actuators.ACTUATOR_LOAD_ASSETS:
            actuator = actuators.LoadAssetsActuatorDrawWindow(
                self, get_assets_func=self.__get_assets_list
            )

        if actuator:
            self.actuators.append(actuator)
            actuator.center()

    def __get_assets_list(self):
        return self.master.get_assets_dict()

    def __get_scene_list(self):
        '''
        this function returns a list with all scenes
        '''
        return self.master.get_scene_list()

    def add_connect_by_AND(self, sensor, actuator):
        and_brick = controllers.ANDControllerDrawWindow(self)
        and_brick.x = 270
        and_brick.y = sensor.y
        self.controllers.append(and_brick)
        self.actuators.append(actuator)
        self.sensors.append(sensor)
        sensor.emissor.connect(and_brick.receptor)
        and_brick.emissor.connect(actuator.receptor)

    def show(self):
        self.deiconify()
        self.center()
        # passing keyboardfocus to the window:
        self.grab_set()

    def hide(self):
        self.grab_release()
        self.withdraw()
        self.master.focus_force()