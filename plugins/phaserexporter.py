# coding: utf-8

import boring.dialog
import boring.form
import posixpath
import shutil
import os

title = 'Export to Phaser'

def read_template(template):
    a = open(template)
    content = a.read()
    a.close()
    return content

MAIN_JS_TEMPLATE = u''
BOOT_JS_TEMPLATE = u''
PRELOAD_JS_TEMPLATE = u''
INDEX_HTML_TEMPLATE = u''
PHASER_CDN = u'https://cdnjs.cloudflare.com/ajax/libs/phaser/2.4.6/phaser.min.js'
PHASER_IMPORT_TAG = u'<script src="{url}"></script>'

def replace_many(string, _dict):
    for key, value in _dict.items():
        string = string.replace(key, value)
    return string

def mkdir(directory):
    '''
    creates a folder/directory
    '''
    if posixpath.exists(directory):
        return
    try:
        os.makedirs(directory)
    except Exception, e:
        print e

FORM_STRING = '''
Export path@string
Loading text@string
Author@string
Email@string
Use Phaser CDN@check
'''

class ExporterWindow(boring.dialog.DefaultDialog):
    def body(self, master):
        self.ide = master
        self.form = boring.form.FormFrame(
            master,
            FORM_STRING,
            initial_values=[
                '',
                'Loading...', '', '', False
            ]
        )
        self.form.pack()
        return self.form

    def apply(self):
        self.create_project_structure()
        self.create_boot_js()
        self.create_preload_js()
        self.create_main_js()
        self.copy_default_images()
        self.create_index_html()

    def create_index_html(self):
        index_html = open(posixpath.join(self.form.values[0], 'index.html'), 'w')
        index_html.write(self.get_index_html())
        index_html.close()

    def get_index_html(self):
        url = 'js/phaser.min.js'
        if self.form.values[3]:
            url = PHASER_CDN
        import_tag = replace_many(PHASER_IMPORT_TAG, {
            '{url}': url
        })
        return replace_many(INDEX_HTML_TEMPLATE, {
            '{phaserscript}': import_tag
        })


    def create_main_js(self):
        main_js = open(posixpath.join(self.form.values[0], 'js/main.js'), 'w')
        main_js.write(self.get_main_js())
        main_js.close()

    def create_boot_js(self):
        boot_file = open(posixpath.join(self.form.values[0], 'js/boot.js'), 'w')
        boot_file.write(self.get_boot_js())
        boot_file.close()

    def create_preload_js(self):
        preload_file = open(posixpath.join(self.form.values[0], 'js/preload.js'), 'w')
        preload_file.write(self.get_preload_js())
        preload_file.close()

    def copy_default_images(self):
        shutil.copy(
            'plugins/phaserexporterassets/loading.png',
            posixpath.join(self.form.values[0], 'assets/images')
        )
        if not self.form.values[3]: # use cdn
            shutil.copy(
                'plugins/phaserexporterassets/phaser.min.js',
                posixpath.join(self.form.values[0], 'js')
            )

    def get_preload_js(self):
        return replace_many(PRELOAD_JS_TEMPLATE, {
            '{loading_text}': self.form.values[1],
            '{game_height}': unicode(self.parent.current_project.height),
            '{loadings}': self.get_loadings_strings()
        })

    def get_boot_js(self):
        return replace_many(BOOT_JS_TEMPLATE, {
            '{bgcolor}': self.parent.current_project.bgcolor.replace('#', '0x'),
        })

    def get_main_js(self):
        return replace_many(MAIN_JS_TEMPLATE, {
            '{gamename}': unicode(self.parent.current_project.name),
            '{gamewidth}': unicode(self.parent.current_project.width),
            '{gameheight}': unicode(self.parent.current_project.height),
            '{author}': self.form.values[2],
            '{authoremail}': self.form.values[3]
        })

    def get_loadings_strings(self, tab_width=2):
        final = u''
        tab = ' ' * tab_width * 4 # 4 spaces
        image_template = u'this.game.load.image("{assetname}","assets/images/{assetname}.{fileextension}");'

        assets = self.parent.get_assets_dict()
        for i in assets:
            if i['type'] == 'image':
                final += replace_many(image_template, {
                    '{assetname}': i['name'],
                    '{fileextension}': i['path'].split('.')[-1].lower()
                }) + '\n' + tab
        return final

    def validate(self):
        if posixpath.isdir(self.form.values[0]):
            return True
        else:
            boring.dialog.MessageBox.warning(
                parent=self,
                title='Wrong path',
                message='The export path is not a valid folder'
            )
            return False

    def create_project_structure(self):
        prefix = self.form.values[0].replace('\\', '/')
        mkdir(posixpath.join(prefix, 'js'))
        mkdir(posixpath.join(prefix, 'assets'))
        mkdir(posixpath.join(prefix, 'assets/images'))
        mkdir(posixpath.join(prefix, 'assets/audio'))

def init(ide):
    pass

def execute(ide):
    global MAIN_JS_TEMPLATE, BOOT_JS_TEMPLATE, PRELOAD_JS_TEMPLATE, INDEX_HTML_TEMPLATE
    BOOT_JS_TEMPLATE = read_template('plugins/phaserexporterassets/BOOT_JS_TEMPLATE')
    MAIN_JS_TEMPLATE = read_template('plugins/phaserexporterassets/MAIN_JS_TEMPLATE')
    PRELOAD_JS_TEMPLATE = read_template('plugins/phaserexporterassets/PRELOAD_JS_TEMPLATE')
    INDEX_HTML_TEMPLATE = read_template('plugins/phaserexporterassets/INDEX_HTML_TEMPLATE')

    if ide.current_project:
        ExporterWindow(ide)
    else:
        boring.dialog.MessageBox.warning(
            parent=ide,
            title='No project loaded',
            message='No project loaded'
        )