# Gator Engine Editor - Auto generated file - Modify loading custom resources

from gator.resources.texture import Texture
from gator.graphics.shader import Shader
from gator.resources.assets import Assets

# User must use this constants as the might be modified at export time for them to work properly
PROJECT_PATH = "projects/GatorEngine_pong/"
ASSETS_PATH = PROJECT_PATH+"assets/"
IMAGES_PATH = ASSETS_PATH+"images/"
SHADERS_PATH = ASSETS_PATH+"shaders/"

def loadResources():
    Assets.registerTexture("circle", Texture(IMAGES_PATH+"circle.png"))
