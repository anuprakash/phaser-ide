# logiceditor:sensors
import boring.drawwidgets
import boring.draw
import boring.form

SENSOR_SIGNAL = 0
SENSOR_ALWAYS = 1
SENSOR_KEYBOARD = 2
SENSOR_JOYSTICK = 3
SENSOR_MOUSE = 4 # TODO: permitir selecionar o objeto
SENSOR_MESSAGE = 5
SENSOR_PROPERTY = 6
SENSOR_COLLISION = 7


class GenericSensorDrawWindow(boring.drawwidgets.DrawWindow):
    def __init__(self, canvas, title='Sensor', widget=None):
        self.__connector = boring.draw.OvalDraw(
            canvas,
            -10,
            -10,
            5,
            5
        )
        boring.drawwidgets.DrawWindow.__init__(
            self,
            canvas,
            fill='#aaa',
            radius=[3]*4,
            title=title,
            widget=widget
        )

    def update(self):
        boring.drawwidgets.DrawWindow.update(self)
        self.__connector.x = self.x + self.width + 5
        self.__connector.y = self.y + 2

    def delete(self):
        boring.drawwidgets.DrawWindow.delete(self)
        self.__connector.delete()

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