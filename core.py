import json

'''
<AssetStructure>
{
    "type": "image, sprite, music, effect",
    "path": "file path",
    "name": "key value"

    if "type" == "sprite":
        "sprite_width": "how many images the source have in horizontal",
        "sprite_height": "the same in vertical",
        "autoplay": "when true begins the sprite sheet animation",
        "framerate": "how many frames per second"
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
'''

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
        self.bgcolor = '#dadada'

        if json:
            self.fill_from_json(json)

    def get_scenes_dict(self):
        return [i.get_dict() for i in self.scenes]

    def load_scenes_from_dict(self, _dict):
        self.scenes = [PhaserScene(i) for i in _dict]

    def fill_from_dict(self, _dict):
        self.name = _dict['name']
        self.width = _dict['width']
        self.height = _dict['height']
        self.bgcolor = _dict['bgcolor']
        self.load_scenes_from_dict(_dict['scenes'])

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