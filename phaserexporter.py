from windows import *

title = 'Export to Phaser'

class ExporterWindow(DefaultDialog):
	pass

def init(ide):
	print 'INIT!@'

def execute(ide):
	ExporterWindow(ide)