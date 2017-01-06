# coding: utf-8

import boring.dialog
import boring.form
import posixpath
import shutil
import os
import logiceditor.sensors
import logiceditor.actuators

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
SCENE_TEMPLATE = u''

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
    def get_asset_path(self, asset_detail):
        '''
        returns the new path in the exported folder
        '''
        if asset_detail['type'] == 'image':
            ext = asset_detail['path'].split('.')[-1].lower()
            return 'assets/images/%s.%s' % (asset_detail['name'], ext)

    def get_loading_js_of_asset(self, assetname):
        '''
        returns the javascript code to load a asset
        '''
        asset_detail = self.ide.get_asset_details_by_name(assetname)
        if asset_detail and asset_detail['type'] == 'image':
            return replace_many('this.game.load.image("{assetname}", "{assetpath}");', {
                '{assetname}': assetname,
                '{assetpath}': self.get_asset_path(asset_detail)
            })
        return None

    def get_load_scene_js_code(self, scenename):
        return replace_many('this.game.state.start("{scenename}");\n', {
            '{scenename}': scenename
        })

    def get_js_code_of_actuator(self, jscode):
        return replace_many(
            jscode,
            self.get_project_properties()
        )

    def get_project_properties(self):
        return {
            '{bgcolor}': self.get_project_bgcolor(),
            '{gamewidth}': self.get_project_width(),
            '{gameheight}': self.get_project_height(),
            '{gamename}': self.get_project_name(),
            '{author}': self.form.values[2],
            '{authoremail}': self.form.values[3]
        }

    def get_project_name(self):
        return unicode(self.ide.current_project.name)

    def get_project_width(self):
        return unicode(self.ide.current_project.width)

    def get_project_height(self):
        return unicode(self.ide.current_project.height)

    def get_actuator_js_code(self, actuator):
        '''
        returns the javascript code of actuator
        '''
        final_js = u''
        actuator_type = type(actuator)
        if actuator_type == logiceditor.actuators.LoadAssetsActuatorDrawWindow:
            for i in actuator.value:
                final_js += self.get_loading_js_of_asset(i) + '\n'
        elif actuator_type == logiceditor.actuators.CodeActuatorDrawWindow:
            return self.get_js_code_of_actuator(actuator.value)
        elif actuator_type == logiceditor.actuators.LoadSceneActuatorDrawWindow:
            return self.get_load_scene_js_code(actuator.value)
        return final_js

    def body(self, master):
        self.ide = master.master.master
        self.form = boring.form.FormFrame(
            master,
            FORM_STRING,
            initial_values=[
                '/home/cptx032/Desktop/john',
                'Loading...', '', '', False
            ]
        )
        self.form.pack()
        return self.form

    def apply(self):
        self.create_project_structure()
        self.create_main_js() # TODO: remove
        self.copy_default_images()
        self.create_index_html()
        # TODO: for each scene do ...
        self.create_scene('boot')

    def create_scene(self, scenename):
        scene_js = open(posixpath.join(self.form.values[0], 'js/%s.js' % (scenename)), 'w')
        scene_js.write(self.get_scene_html(scenename))
        scene_js.close()

    def get_scene_html(self, scenename):
        return replace_many(SCENE_TEMPLATE, {
            '{preload}': self.get_scene_preload_js(scenename),
            '{create}': self.get_scene_create_js(scenename),
            '{update}': self.get_scene_update_js(scenename),
            '{scenename}': scenename
        })

    def get_scene_update_js(self, scenename):
        final_js = u''
        for controller in self.ide.logic_editors[scenename].controllers:
            if type(controller) == logiceditor.controllers.ANDControllerDrawWindow:
                # print controller.actuator
                # getting sensors
                conditions = []
                for sensor in controller.sensors:
                    js_condition = self.get_sensor_js_condition(sensor)
                    if js_condition:
                        conditions.append(js_condition)
                if conditions:
                    conditions_in_js = 'if (%s)' % (self.get_js_of_conditions(conditions))
                    print conditions_in_js
            elif type(controller) == logiceditor.controllers.ORControllerDrawWindow:
                pass
        return final_js

    def get_js_of_conditions(self, conditions):
        to_join = []
        for i in conditions:
            if type(i) == str:
                to_join.append('(%s)' % (i))
        return ' && '.join(to_join)

    def get_sensor_js_condition(self, sensor):
        """
        Can return True if is always, string, width js condition
        or False to not be considered
        """
        if type(sensor) == logiceditor.sensors.PreloadSensorDrawWindow:
            return False
        elif type(sensor) == logiceditor.sensors.SignalSensorDrawWindow:
            return False
        elif type(sensor) == logiceditor.sensors.AlwaysSensorDrawWindow:
            return True
        elif type(sensor) == logiceditor.sensors.MessageSensorDrawWindow:
            return 'window.phasermessages.indexOf("%s") != -1' % (sensor.subject)
        return None

    def get_js_code_of_a_sensor(self, scenename, sensortype):
        final_js = ''
        for sensor in self.ide.logic_editors[scenename].sensors:
            if type(sensor) == sensortype:
                controller = sensor.receptor_brick_connected
                if controller:
                    actuator = controller.receptor_brick_connected
                    if actuator:
                        final_js += self.get_actuator_js_code(actuator) + '\n'
        return final_js

    def get_scene_create_js(self, scenename):
        return self.get_js_code_of_a_sensor(
            scenename,
            logiceditor.sensors.SignalSensorDrawWindow
        )

    def get_scene_preload_js(self, scenename):
        return self.get_js_code_of_a_sensor(
            scenename,
            logiceditor.sensors.PreloadSensorDrawWindow
        )

    def create_index_html(self):
        index_html = open(posixpath.join(self.form.values[0], 'index.html'), 'w')
        index_html.write(self.get_index_html())
        index_html.close()

    def get_index_html(self):
        url = 'js/phaser.min.js'
        if self.form.values[4]:
            url = PHASER_CDN
        import_tag = replace_many(PHASER_IMPORT_TAG, {
            '{url}': url
        })
        return replace_many(INDEX_HTML_TEMPLATE, {
            '{phaserscript}': import_tag,
            '{gamename}': self.parent.current_project.name
        })


    def create_main_js(self):
        main_js = open(posixpath.join(self.form.values[0], 'js/main.js'), 'w')
        main_js.write(self.get_main_js())
        main_js.close()

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

    def get_project_bgcolor(self):
        return self.ide.current_project.bgcolor.replace('#', '0x')

    def get_main_js(self):
        return replace_many(MAIN_JS_TEMPLATE, {
            '{gamename}': unicode(self.parent.current_project.name),
            '{gamewidth}': unicode(self.parent.current_project.width),
            '{gameheight}': unicode(self.parent.current_project.height),
            '{author}': self.form.values[2],
            '{authoremail}': self.form.values[3]
        })

    def get_loadings_strings(self, tab_width=2): # TODO: remove
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
    global MAIN_JS_TEMPLATE, BOOT_JS_TEMPLATE, PRELOAD_JS_TEMPLATE,\
            INDEX_HTML_TEMPLATE, SCENE_TEMPLATE
    BOOT_JS_TEMPLATE = read_template('plugins/phaserexporterassets/BOOT_JS_TEMPLATE')
    MAIN_JS_TEMPLATE = read_template('plugins/phaserexporterassets/MAIN_JS_TEMPLATE')
    PRELOAD_JS_TEMPLATE = read_template('plugins/phaserexporterassets/PRELOAD_JS_TEMPLATE')
    INDEX_HTML_TEMPLATE = read_template('plugins/phaserexporterassets/INDEX_HTML_TEMPLATE')
    SCENE_TEMPLATE = read_template('plugins/phaserexporterassets/SCENE_TEMPLATE')

    if ide.current_project:
        ExporterWindow(ide)
    else:
        boring.dialog.MessageBox.warning(
            parent=ide,
            title='No project loaded',
            message='No project loaded'
        )