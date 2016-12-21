# coding: utf-8

import boring.dialog
import boring.form
import posixpath
import shutil
import os

title = 'Export to Phaser'

MAIN_JS_TEMPLATE = '''
/*
Author: {author}
Email: {authoremail}
*/

function main()
{
    (function()
    {
        var game = new Phaser.Game({gamewidth}, {gameheight}, Phaser.AUTO, '{gamename}');
        game.state.add("Boot", boot);
        game.state.add("PortraitMode", boot);
        game.state.add("Preload", preload);
        game.state.add("Game", phase01);
        game.state.start("Boot");
    }());
}
'''

BOOT_JS_TEPLATE = '''
var boot = function(game){};
boot.prototype = {
    preload: function()
    {
        this.game.load.image("loading","assets/images/loading.png");
    },
    create: function()
    {
        this.game.debug.text("BOOT",0,10);
        this.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
        this.game.stage.scale.forceLandscape = true;

        this.scale.pageAlignHorizontally = true;
        this.scale.pageAlignVertically = true;
        this.game.stage.backgroundColor = {bgcolor};
        this.game.scale.forceOrientation(true, false);

        this.game.scale.enterIncorrectOrientation.add(this.handleIncorrect);

        this.game.state.start("Preload");
    },
    handleIncorrect: function()
    {
        alert('para uma melhor experiência utilize seu dispositivo na orientação horizontal');
    }
}
'''

PRELOAD_JS_TEMPLATE = '''
var preload = function(game){}
preload.prototype = {
    preload: function()
    {
        this.game.debug.text("{loading_text}", this.game.world.centerX, this.game.world.centerY);
        var loadingBar = this.add.sprite(0, {game_height}, "loading");
        loadingBar.anchor.setTo(0.0, 1.0);
        this.load.setPreloadSprite(loadingBar);
        {loadings}
    },
    create: function()
    {
        this.game.state.start('Game');
    },
    update: function() {
    }
}
'''

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

class ExporterWindow(boring.dialog.DefaultDialog):
    def body(self, master):
        self.ide = master
        self.form = boring.form.FormFrame(
            master,
            'Export path@string\nLoading text@string\nAuthor@string\nEmail@string',
            initial_values=[
                '',
                'Loading...', '', ''
            ]
        )
        self.form.pack()
        return self.form

    def apply(self):
        self.create_project_structure()

    def get_preload_js(self):
        return replace_many(PRELOAD_JS_TEMPLATE, {
            '{loading_text}': self.form.values[1],
            '{game_height}': unicode(self.parent.current_project.height),
            '{loadings}': self.get_loadings_strings()
        })

    def get_boot_js(self):
        return replace_many(BOOT_JS_TEPLATE, {
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
    if ide.current_project:
        ExporterWindow(ide)
    else:
        boring.dialog.MessageBox.warning(
            parent=ide,
            title='No project loaded',
            message='No project loaded'
        )