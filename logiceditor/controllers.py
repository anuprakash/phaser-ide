# logiceditor:controllers

import core

CONTROLLER_AND = 0
CONTROLLER_OR = 1

class GenericControllerDrawWindow(core.GenericLogicEditorDrawWindow):
    def __init__(self, logiceditor, title='Controller', widget=None):
        core.GenericLogicEditorDrawWindow.__init__(
            self,
            logiceditor,
            fill='#34495e',
            radius=[5,0,0,5],
            title=title,
            widget=widget,
            emissor=True,
            receptor=True,
            receptor_type='controller',
            emissor_type='controller',
            close_function=self.__remove_controller
        )

    def __remove_controller(self, event=None):
        self.logiceditor.controllers.remove(self)

    @property
    def actuator(self):
        return self.receptor_brick_connected

    @property
    def sensors(self):
        return_sensors = []
        for string in self.receptor.strings:
            return_sensors.append(string.obj1.draw_window)
        return return_sensors

class ANDControllerDrawWindow(GenericControllerDrawWindow):
    def __init__(self, logiceditor):
        GenericControllerDrawWindow.__init__(
            self,
            logiceditor,
            title='AND'
        )

class ORControllerDrawWindow(GenericControllerDrawWindow):
    def __init__(self, logiceditor):
        GenericControllerDrawWindow.__init__(
            self,
            logiceditor,
            title='OR'
        )