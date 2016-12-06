from . import *
import string

FORMSTRING = '''
Name@string
'''

class AddSceneWindow(DefaultDialog):
	def body(self, master):
		self.output = None
		self.form = FormFrame(master, FORMSTRING)
		self.form.grid(pady=10, padx=10)
		self.form.inputs[0].allowsonly = list(string.letters)
		return self.form.inputs[0]

	def validate(self):
		if not self.form.values[0]:
			MessageBox.warning(parent=self,
				title='Invalid name',
				message='Enter a valid name')
			return False
		return True

	def apply(self):
		self.output = {
			"name": self.form.values[0]
		}