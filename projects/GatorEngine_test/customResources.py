from gator.resources.texture import Texture
from gator.resources.assets import Assets

PROJECT_PATH = "projects/GatorEngine_test/"
ASSETS_PATH = PROJECT_PATH+"assets/"
IMAGES_PATH = ASSETS_PATH+"images/"

def loadResources():
    Assets.registerTexture("purplebg", Texture(IMAGES_PATH+"purplebg.png"))