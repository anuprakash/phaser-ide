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

class Asset:
    def __init__(self, json=None):
        self.name = ''
        if json:
            self.fill_from_json(json)

    def get_json(self):
        '''
        returns the json representation of scene
        '''
        _dict = {
            'name': self.name
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

    def load_assets_from_json(self, json):
        print json
    
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
        self.assets = self.load_assets_from_json(_dict['assets'])
        self.scenes = [PhaserScene(i) for i in _dict['scenes']]

    def get_json(self):
        '''
        returns the json representation of project
        '''
        print self.assets
        _dict = {
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'scenes': [i.get_json() for i in self.scenes],
            'assets': self.get_assets_json()
        }
        return json.dumps(_dict)