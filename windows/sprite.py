from . import *

class SpriteImagePropertyWindow(DefaultDialog):
    def body(self, master):
        self.output = None
        return None

    def validate(self):
        return True

    def apply(self):
        self.output = {
        }