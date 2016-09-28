class BaseDraw(object):
	"""
	This class represents a basic draw.
	I think that you will never use this class, but understand how it
	works is good for understand lightk.
	"""
	def __init__(self, canvas, *coords, **style):
		self.canvas = canvas
		self.coords = list(coords)
		self.style = style
		self.index = self.draw()
	def draw(self):
		""" Must return the the canvas draw's index """
		pass
	def get_coords(self):
		'''
		must return the coords
		'''
		raise NotImplementedError
	def update(self, **kws):
		"""
		This method updates the position and the attributes of an object.
		If you pass the 'idle' arg with True, so lightk will force the draw
		calling 'Tkinter.Canvas.update_idletasks' method.
		Recomendation: If you are updating a list of many objects use idle=True
		only in the last object, because this will force the updating of all:
			obj01.update()
			obj02.update()
			obj03.update(idle=True)
		"""
		self.coords = self.get_coords()
		if self.index:
			self.canvas.coords(self.index, *self.coords)
			self.canvas.itemconfig(self.index, **self.style)
			if kws.get("idle",False):
				self.canvas.update_idletasks()
	def to_raise(self):
		"""
		This method puts the object in the top of all objects.
		Use this function if you want have certain that your
		object will be looked.
		"""
		self.canvas.tag_raise(self.index)
	def to_lower(self):
		"""
		This method puts the object in the down of all objects.
		"""
		self.canvas.lower(self.index)
	def bind(self, *args, **kargs):
		"""
		This method works like 'Tkinter.Widget.bind': binds a functions
		to an event.
		"""
		self.canvas.tag_bind(self.index, *args, **kargs)
	def destroy(self):
		"""
		This method will delete the object and clean the index to None.
		To re-activate the object call 'obj.init()'
		"""
		self.canvas.delete(self.index)
		self.index = None

class Rectangle(BaseDraw):
	def __init__(self, canvas, x=0, y=0, width=10, height=10, **style):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		BaseDraw.__init__(self, canvas, self.get_coords(), **style)
	def draw(self):
		return self.canvas.create_rectangle(self.x,
			self.y, self.x+self.width,
			self.y+self.height, **self.style)
	def get_coords(self):
		return [self.x, self.y, self.x+self.width, self.y+self.height]
	@property
	def width(self):
		return self.__width
	@width.setter
	def width(self, value):
		self.__width = value
		self.update()
	@property
	def height(self):
		return self.__height
	@height.setter
	def height(self, value):
		self.__height = value
		self.update()
	@property
	def x(self):
		return self.__x
	@x.setter
	def x(self, value):
		self.__x = value
		self.update()
	@property
	def y(self):
		return self.__y
	@y.setter
	def y(self, value):
		self.__y = value
		self.update()

class Oval(Rectangle):
	def draw(self):
		return self.canvas.create_oval(self.x,
			self.y, self.x+self.width,
			self.y+self.height, **self.style)
	@property
	def radius(self):
		if self.width == self.height:
			return self.width
		else:
			return None
	@radius.setter
	def radius(self, value):
		self.width = value*2
		self.height = value*2

def __drag_callback(control, event, endfunc):
	# fixme: verificar se o control esta ativo e
	# dar um lock soh em x ou soh em y
	control.x = event.x
	control.y = event.y
	if endfunc:
		endfunc()

def drag_control(control, callback=None):
	control.bind('<B1-Motion>', lambda evt: __drag_callback(control, evt, callback), '+' )

if __name__ == '__main__':
	def _in_drag(*args):
		pass
	from Tkinter import *
	top = Tk()
	ca = Canvas(top, highlightthickness=0, bg='white')
	ca.grid()
	rec = Rectangle(ca, 0,0, width=100, height=100, fill="black")
	rec.x = 10
	rec.width = 100
	drag_control(rec, _in_drag)
	top.mainloop()