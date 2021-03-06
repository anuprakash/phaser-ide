import boring.dialog
import boring.form
import string

FORMSTRING = '''
Name@string
'''

class AddSceneWindow(boring.dialog.DefaultDialog):
	def body(self, master):
		self.output = None
		self.form = boring.form.FormFrame(
			master, FORMSTRING, title='Add scene'
		)
		self.form.grid(pady=10, padx=10)
		self.form.inputs[0].allowsonly = list(string.letters)
		return self.form.inputs[0]

	def validate(self):
		if not self.form.values[0]:
			boring.dialog.MessageBox.warning(parent=self,
				title='Invalid name',
				message='Enter a valid name')
			return False
		return True

	def apply(self):
		self.output = {
			'name': self.form.values[0]
		}