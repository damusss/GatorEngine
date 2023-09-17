

class AppSettings:
    def __init__(self, width: int | str, height: int | str, title: str, sceneName: str, projectName: str):
        self.width: int | str = width
        self.height: int | str = height
        self.title: str = title
        self.sceneName: str = sceneName
        self.projectName: str = projectName


EMPTY_PROJECT_MAIN_SCENE = '{"entities": [], "inactiveEntities": [], "camera": {"pos": [0.0, 0.0, 0.0], "zoom": 1}, "clearColor": [0.0, 0.0, 0.0, 1.0]}'
EMPTY_PROJECT_COMPS_MODULE = """# Gator Engine Editor - Auto generated file - Modify with custom components
from gator.components.all import *

allComponents = [
    Transform,
    SpriteRenderer
]
"""
