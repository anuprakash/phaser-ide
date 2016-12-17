# logic editor
import boring.dialog
import boring.widgets
import boring.drawwidgets
import boring.menus
from boring import *
import sensors
import controllers
import actuators


class LogicEditor(boring.dialog.DefaultDialog):
    def body(self, master):
        self.canvas = boring.widgets.ExtendedCanvas(
            master,
            relief='flat',
            bd=0,
            highlightthickness=0,
            bg='#ededed'
        )
        self.canvas.pack(
            expand='yes',
            fill='both'
        )

        self.__menu = boring.menus.CommandChooserWindow(
            self,
            items=[
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
                    command=lambda *args : self.__add_actuator(actuators.ACTUATOR_CODE)
                ),
                dict(
                    name='Add Mouse Visibility Actuator',
                    command=lambda *args: self.__add_actuator(actuators.ACTUATOR_MOUSE_VISIBILITY)
                ),
            ]
        )
        self.bind(
            '<Control-space>',
            lambda evt: self.__menu.show(),
            '+'
        )
        self.__menu.withdraw()

        self.resizable(1, 1)
        # TODO: maximize in Windows
        self.attributes('-zoomed', 1)
        return self.canvas

    def __add_sensor(self, sensor_type):
        if sensor_type == sensors.SENSOR_MESSAGE:
            sensors.MessageSensorDrawWindow(self.canvas).center()
        elif sensor_type == sensors.SENSOR_SIGNAL:
            sensors.SignalSensorDrawWindow(self.canvas).center()
        elif sensor_type == sensors.SENSOR_ALWAYS:
            sensors.AlwaysSensorDrawWindow(self.canvas).center()

    def __add_controller(self, controller_type):
        if controller_type == controllers.CONTROLLER_AND:
            controllers.ANDControllerDrawWindow(self.canvas).center()
        elif controller_type == controllers.CONTROLLER_OR:
            controllers.ORControllerDrawWindow(self.canvas).center()

    def __add_actuator(self, actuator_type):
        if actuator_type == actuators.ACTUATOR_QUIT_GAME:
            actuators.QuitGameActuatorDrawWindow(self.canvas).center()
        elif actuator_type == actuators.ACTUATOR_RESTART_GAME:
            actuators.RestartGameActuatorDrawWindow(self.canvas).center()
        elif actuator_type == actuators.ACTUATOR_RESTART_SCENE:
            actuators.RestartSceneActuatorDrawWindow(self.canvas).center()
        elif actuator_type == actuators.ACTUATOR_CODE:
            actuators.CodeActuatorDrawWindow(self.canvas).center()
        elif actuator_type == actuators.ACTUATOR_MOUSE_VISIBILITY:
            actuators.MouseVisibilityActuatorDrawWindow(self.canvas).center()

    def buttonbox(self):
        pass