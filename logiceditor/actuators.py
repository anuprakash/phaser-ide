# logiceditor:actuators

import boring.drawwidgets

ACTUATOR_CODE = 0
ACTUATOR_SCENE = 1
ACTUATOR_GAME = 2

class GenericActuatorDrawWindow(boring.drawwidgets.DrawWindow):
    def __init__(self, canvas, title='Actuator', widget=None):
        self.__connector_right = boring.draw.OvalDraw(
            canvas,
            -10,
            -10,
            5,
            5
        )
        boring.drawwidgets.DrawWindow.__init__(
            self,
            canvas,
            fill='#cccccc',
            radius=[3]*4,
            title=title,
            widget=widget
        )

    def update(self):
        boring.drawwidgets.DrawWindow.update(self)
        self.__connector_right.x = self.x + self.width + 5
        self.__connector_right.y = self.y + 2

    def delete(self):
        boring.drawwidgets.DrawWindow.delete(self)
        self.__connector_right.delete()