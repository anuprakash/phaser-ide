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
    "scenes": [<SceneStructure>, ...],
    "bgcolor": "background color rgb"
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

class DuplicatedAssetNameException(Exception):
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
        _dict = {
            'name': self.name,
            'path': self.path,
            'type': self.type
        }
        if self.type == 'sprite':
            _dict.update(sprite_width=self.sprite_width,
                sprite_height=self.sprite_height,
                autoplay=self.autoplay,
                framerate=self.framerate)
        return _dict

    def fill_from_dict(self, _dict):
        self.name = _dict['name']
        self.type = _dict['type']
        self.path = _dict['path']

        if self.type == 'sprite':
            self.sprite_width = _dict['sprite_width']
            self.sprite_height = _dict['sprite_height']
            self.autoplay = _dict['autoplay']
            self.framerate = _dict['framerate']

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
        self.bgcolor = '#dadada'

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
        self.bgcolor = _dict['bgcolor']
        self.load_assets_from_dict(_dict['assets'])
        self.load_scenes_from_dict(_dict['scenes'])

    def assets_exists_by_name(self, name):
        for i in self.assets:
            if i.name == name:
                return True
        return False

    def add_asset(self, asset):
        if self.assets_exists_by_name(asset.name):
            raise DuplicatedAssetNameException()
        self.assets.append(asset)

    def get_json(self):
        '''
        returns the json representation of project
        '''
        _dict = {
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'scenes': self.get_scenes_dict(),
            'assets': self.get_assets_dict(),
            'bgcolor': self.bgcolor
        }
        return json.dumps(_dict)

    def get_asset_from_name(self, name):
        '''
        returns the path in physical hard drive of sprite
        using its name
        '''
        for i in self.assets:
            if i.name == name:
                return i
        return None