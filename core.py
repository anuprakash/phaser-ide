import json

'''
<assetStructure>
{
    "type": "image, sprite, music, effect",
    "path": "file path",
    "name": "key value"
}

<PhaserProject>
{
    "name": "name",
    "width": "width",
    "height": "height",
    "assets": [<assetStructure>, ...],
    "scenes": [<SceneStructure>, ...]
}

<SceneStructure>
{
    "name": "name",
    "sprites": [<SpriteStructure>, ...]
}

<SpriteStructure>
{
    TODO
}
'''

class DuplicatedSceneNameException(Exception):
    pass

class Asset:
    def __init__(self, json=None):
        self.name = ''
        self.path = ''
        self.type = ''
        if json:
            self.fill_from_json(json)

    def get_json(self):
        '''
        returns the json representation of scene
        '''
        _dict = {
            'name': self.name,
            'path': self.path,
            'type': self.type
        }
        return json.dumps(_dict)

    def fill_from_json(self, jsonstring):
        '''
        args:
            + json: json string

        fills the instance with data from json string
        '''
        _dict = json.loads(jsonstring)
        self.name = _dict['name']
        self.type = _dict['type']
        self.path = _dict['path']

# only allow edits the events of scene: onframe, onstart
class PhaserScene:
    def __init__(self, json=None):
        self.name = ''
        self.sprites = []
        if json:
            self.fill_from_json(json)

    def get_json(self):
        '''
        returns the json representation of scene
        '''
        _dict = {
            'name': self.name,
            'sprites': [i.get_json() for i in self.sprites]
        }
        return json.dumps(_dict)

    def fill_from_json(self, jsonstring):
        '''
        args:
            + json: json string

        fills the instance with data from json string
        '''
        _dict = json.loads(jsonstring)
        self.name = _dict['name']
        self.sprites = [] # TODO

# fixme: raise NotSavedProjectException
class PhaserProject:
    def __init__(self, json=None):
        self.json = json
        self.name = ''
        self.width = 640
        self.height = 480
        self.scenes = []
        self.assets = []

        if json:
            self.fill_from_json(json)

    def get_assets_json(self):
        return json.dumps([i.get_json() for i in self.assets])

    def get_scenes_json(self):
        return json.dumps([i.get_json() for i in self.scenes])

    def load_assets_from_json(self, _json):
        self.assets = [Asset(i) for i in json.loads(_json)]
    
    def fill_from_json(self, jsonstring):
        '''
        args:
            + json: json string

        fills the instance with data from json string
        '''
        _dict = json.loads(jsonstring)
        self.name = _dict['name']
        self.width = _dict['width']
        self.height = _dict['height']
        self.load_assets_from_json(_dict['assets'])
        self.scenes = [PhaserScene(i) for i in json.loads(_dict['scenes'])]

    def add_scene_from_json(self, json_scene):
        scene = PhaserScene(json_scene)
        for i in self.scenes:
            if i.name == scene.name:
                raise DuplicatedSceneNameException()
        self.scenes.append( PhaserScene(json_scene) )

    def remove_scene_from_name(self, name):
        for i in self.scenes:
            if i.name == name:
                self.scenes.remove(i)

    def get_json(self):
        '''
        returns the json representation of project
        '''
        _dict = {
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'scenes': self.get_scenes_json(),
            'assets': self.get_assets_json()
        }
        return json.dumps(_dict)