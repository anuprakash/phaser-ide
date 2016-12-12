# logiceditor:controllers

import boring.drawwidgets

CONTROLLER_AND = 0
CONTROLLER_OR = 1

class GenericControllerDrawWindow(boring.drawwidgets.DrawWindow):
    def __init__(self, canvas, title='Controller', widget=None):
        self.__connector_left = boring.draw.OvalDraw(
            canvas,
            -10,
            -10,
            5,
            5
        )
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
            fill='#34495e',
            radius=[3]*4,
            title=title,
            widget=widget
        )

    def update(self):
        boring.drawwidgets.DrawWindow.update(self)
        self.__connector_right.x = self.x + self.width + 5
        self.__connector_right.y = self.y + 2

        self.__connector_left.x = self.x - 10
        self.__connector_left.y = self.y + 2

    def delete(self):
        boring.drawwidgets.DrawWindow.delete(self)
        self.__connector_left.delete()
        self.__connector_right.delete()

class ANDControllerDrawWindow(GenericControllerDrawWindow):
    def __init__(self, canvas):
        GenericControllerDrawWindow.__init__(
            self,
            canvas,
            title='AND'
        )

class ORControllerDrawWindow(GenericControllerDrawWindow):
    def __init__(self, canvas):
        GenericControllerDrawWindow.__init__(
            self,
            canvas,
            title='OR'
        )