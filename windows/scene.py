from . import *

class AddSceneWindow(DefaultDialog):
	def body(self, master):
		self.output = None
		Label(master, text="Name").grid(row=0, column=0)
		self.scene_name = Entry(master)
		self.scene_name.grid(row=0, column=1)
		return self.scene_name

	def validate(self):
		if not self.scene_name.get():
			MessageBox.warning(parent=self,
				title='Invalid name',
				message='Enter a valid name')
			return False
		return True

	def apply(self):
		self.output = {
			"name": self.scene_name.get(),
			'sprites': []
		}