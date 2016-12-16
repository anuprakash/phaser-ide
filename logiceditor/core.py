# logiceditor:core

import boring.drawwidgets

class ConnectorString(boring.draw.LineDraw):
    def __init__(self, canvas, obj1=None, obj2=None):
        self.obj1 = obj1
        self.obj2 = obj2
        boring.draw.LineDraw.__init__(
            self, canvas, 0,0,0,0,
            fill='blue'
        )
        self.bind('<Motion>', self.__motion, '+')
        self.bind('<Leave>', self.__leave, '+')

    def __leave(self, event):
        self.style['fill'] = 'blue'
        self.update()

    def __motion(self, event):
        self.style['fill'] = 'red'
        self.update()

    def update_coords(self):
        if self.obj1:
            self.p1 = [self.obj1.center_x, self.obj1.center_y]
        if self.obj2:
            self.p2 = [self.obj2.center_x, self.obj2.center_y]

class ConnectorReceptor(boring.draw.OvalDraw):
    RECEPTORS = []
    def __init__(self, draw_window, receptor_type):
        self.receptor_type = receptor_type
        self.draw_window = draw_window
        self.__strings = []
        boring.draw.OvalDraw.__init__(
            self, draw_window.canvas,
            draw_window.x - 10,
            draw_window.y + 2,
            5, 5
        )
        ConnectorReceptor.RECEPTORS.append(self)

    def add_string_connector(self, string_connector):
        '''
        string_connector is a instance of ConnectorString
        this function is called when the user drags a string
        from a emissor to a receptor
        '''
        self.__strings.append(string_connector)

    # dont override .update because infinity recursion
    # : updating x/y will call .update
    def update_position(self):
        self.x = self.draw_window.x - 10
        self.y = self.draw_window.y + 2
        if self.__strings:
            for i in self.__strings:
                i.update_coords()

class ConnectorEmissor(boring.draw.OvalDraw):
    def __init__(self, draw_window, emissor_type):
        '''
        emissor_type can be sensor or controller
        '''
        self.emissor_type = emissor_type
        self.draw_window = draw_window
        self.__string = None
        boring.draw.OvalDraw.__init__(
            self, draw_window.canvas,
            draw_window.x + draw_window.width + 5,
            draw_window.y + 2,
            5, 5, fill='#ddd'
        )
        self.bind('<B1-Motion>', self.__motion, '+')
        self.bind('<ButtonRelease-1>', self.__button_release, '+')

    def __button_release(self, event):
        if not self.__string.obj2:
            self.__string.delete()
            self.__string = None

    def __valid_connection(self, receptor):
        if self.emissor_type == 'sensor':
            return receptor.receptor_type == 'controller'
        elif self.emissor_type == 'controller':
            return receptor.receptor_type == 'actuator'
        return False

    def __motion(self, event):
        if not self.__string:
            self.__string = ConnectorString(
                self.canvas, obj1=self
            )
        else:
            if not self.__string.obj2:
                self.__string.p2 = [event.x, event.y]
                self.__string.update_coords()
                for receptor in ConnectorReceptor.RECEPTORS:
                    inside = receptor.is_inside(event.x, event.y)
                    valid_connection = self.__valid_connection(receptor)
                    if valid_connection and inside:
                        self.__string.obj2 = receptor
                        receptor.add_string_connector(self.__string)
                        break


    # dont override .update because infinity recursion
    # : updating x/y will call .update
    def update_position(self):
        self.x = self.draw_window.x + self.draw_window.width + 5
        self.y = self.draw_window.y + 2
        if self.__string:
            self.__string.update_coords()

class GenericLogicEditorDrawWindow(boring.drawwidgets.DrawWindow):
    def __init__(self,
            canvas, title='Controller',
            widget=None,
            emissor=True,
            receptor=True,
            fill='#ccc',
            emissor_type=None,
            receptor_type=None,
            radius=[3]*4):
        self.receptor = None
        self.emissor = None
        boring.drawwidgets.DrawWindow.__init__(
            self,
            canvas,
            radius=radius,
            title=title,
            widget=widget,
            fill=fill
        )
        if receptor:
            self.receptor = ConnectorReceptor(
                self, receptor_type=receptor_type
            )
        if emissor:
            self.emissor = ConnectorEmissor(
                self, emissor_type=emissor_type
            )

    def update(self):
        boring.drawwidgets.DrawWindow.update(self)
        if self.emissor:
            self.emissor.update_position()

        if self.receptor:
            self.receptor.update_position()

    def delete(self):
        boring.drawwidgets.DrawWindow.delete(self)
        if self.receptor:
            self.receptor.delete()
        if self.emissor:
            self.emissor.delete()