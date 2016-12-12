# logiceditor:sensors
import boring.drawwidgets

SENSOR_ONCE = 0
SENSOR_ALWAYS = 1
SENSOR_KEYBOARD = 2
SENSOR_JOYSTICK = 3
SENSOR_MOUSE = 4 # TODO: permitir selecionar o objeto
SENSOR_MESSAGE = 5
SENSOR_PROPERTY = 6
SENSOR_COLLISION = 7

class MessageSensorDrawWindow(boring.drawwidgets.DrawWindow):
    pass