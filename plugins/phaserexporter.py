import boring.dialog

title = 'Export to Phaser'

class ExporterWindow(boring.dialog.DefaultDialog):
	pass

def init(ide):
	print('INIT!@')

def execute(ide):
	ExporterWindow(ide)