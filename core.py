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

class PhaserProject:
    def __init__(self, json=None):
        self.json = json
        self.name = ''
        self.width = 640
        self.height = 480
        self.bgcolor = '#dadada'

        if json:
            self.fill_from_json(json)

    def load_scenes_from_dict(self, _dict):
        self.scenes = [PhaserScene(i) for i in _dict]

    def fill_from_dict(self, _dict):
        self.name = _dict['name']
        self.width = _dict['width']
        self.height = _dict['height']
        self.bgcolor = _dict['bgcolor']

    def get_json(self):
        '''
        returns the json representation of project
        '''
        _dict = {
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'bgcolor': self.bgcolor
        }
        return json.dumps(_dict)