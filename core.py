import json

'''
<AssetStructure>
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
    def __init__(self, _dict=None):
        self.name = ''
        self.path = ''
        self.type = ''
        if _dict:
            self.fill_from_dict(_dict)

    def get_json(self):
        '''
        returns the json representation of scene
        '''
        return json.dumps(self.get_dict())

    def get_dict(self):
        return {
            'name': self.name,
            'path': self.path,
            'type': self.type
        }

    def fill_from_dict(self, _dict):
        self.name = _dict['name']
        self.type = _dict['type']
        self.path = _dict['path']

# only allow edits the events of scene: onframe, onstart
class PhaserScene:
    def __init__(self, _dict=None):
        self.name = ''
        self.sprites = []
        if _dict:
            self.fill_from_dict(_dict)

    def get_json(self):
        '''
        returns the json representation of scene
        '''
        return json.dumps(self.get_dict())

    def get_dict(self):
        return {
            'name': self.name,
            'sprites': [i.get_dict() for i in self.sprites]
        }

    def fill_from_dict(self, _dict):
        self.name = _dict['name']
        self.sprites = []

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

    def get_assets_dict(self):
        return [i.get_dict() for i in self.assets]

    def get_scenes_dict(self):
        return [i.get_dict() for i in self.scenes]

    def load_assets_from_dict(self, _dict):
        self.assets = [Asset(i) for i in _dict]

    def load_scenes_from_dict(self, _dict):
        self.scenes = [PhaserScene(i) for i in _dict]

    def fill_from_dict(self, _dict):
        self.name = _dict['name']
        self.width = _dict['width']
        self.height = _dict['height']
        self.load_assets_from_dict(_dict['assets'])
        self.load_scenes_from_dict(_dict['scenes'])

    # TODO: remove
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
            'scenes': self.get_scenes_dict(),
            'assets': self.get_assets_dict()
        }
        return json.dumps(_dict)