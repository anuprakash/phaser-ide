import boring.dialog
import boring.form
import posixpath

title = 'Export to Phaser'

PRELOAD_JS_TEMPLATE = '''
var preload = function(game){}
preload.prototype = {
    preload: function()
    {
        this.game.debug.text("{loading_text}", this.game.world.centerX, this.game.world.centerY);
        this.game.stage.backgroundColor = {bgcolor};
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

class ExporterWindow(boring.dialog.DefaultDialog):
    def body(self, master):
        self.ide = master
        self.form = boring.form.FormFrame(
            master,
            'Export path@string\nLoading text@string',
            initial_values=[
                '',
                'Loading...'
            ]
        )
        self.form.pack()
        return self.form

    def apply(self):
        print('extracting to:', self.form.values[0], '...')
        preload_js = replace_many(PRELOAD_JS_TEMPLATE, {
            '{loading_text}': self.form.values[1],
            '{bgcolor}': self.parent.current_project.bgcolor.replace('#', '0x'),
            '{game_height}': unicode(self.parent.current_project.height),
            '{loadings}': 'TODO'
        })
        print preload_js

        print self.parent.get_assets_dict()

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