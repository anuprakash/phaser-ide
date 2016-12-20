# coding: utf-8
# Author: Willie Lawrence

# Assets Pack

import boring.dialog
import boring.menus

title = 'Assets Pack Importer/Exporter'

class AssetsPackWindow(boring.dialog.DefaultDialog):
	pass

def init(ide):
	pass

def __import_assets_pack(*args):
	print 'import assets pack'

def __export_assets_pack(*args):
	print 'exporting...'

def execute(ide):
	boring.menus.CommandChooserWindow.popup([{
			'name': 'Import pack',
			'subtitle': 'Import a zip file with assets',
			'command': __import_assets_pack,
			'icon': 'icons/folder.png'
		},
		{
			'name': 'Export pack',
			'subtitle': 'Export a zip file with assets',
			'command': __export_assets_pack,
			'icon': 'icons/folder.png'
		}
	])