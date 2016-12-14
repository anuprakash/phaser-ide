# logiceditor:controllers

import core

CONTROLLER_AND = 0
CONTROLLER_OR = 1

class GenericControllerDrawWindow(core.GenericLogicEditorDrawWindow):
    def __init__(self, canvas, title='Controller', widget=None):
        core.GenericLogicEditorDrawWindow.__init__(
            self,
            canvas,
            fill='#34495e',
            radius=[3]*4,
            title=title,
            widget=widget,
            emissor=True,
            receptor=True
        )

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