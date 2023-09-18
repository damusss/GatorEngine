class AppSettings:
    def __init__(self, width: int | str, height: int | str, maximized:bool, title: str, sceneName: str, projectName: str, searchPath: str, allCompsMod, customResMod):
        self.width: int | str = width
        self.height: int | str = height
        self.title: str = title
        self.maximized = maximized
        self.sceneName: str = sceneName
        self.projectName: str = projectName
        self.searchPath: str = searchPath
        self.allCompsMod = allCompsMod
        self.customResMod = customResMod


EMPTY_PROJECT_MAIN_SCENE = '{"entities": [], "inactiveEntities": [], "camera": {"pos": [0.0, 0.0, 0.0], "zoom": 1}, "clearColor": [0.0, 0.0, 0.0, 1.0]}'

EMPTY_PROJECT_COMPS_MODULE = """# Gator Engine Editor - Auto generated file - Modify with custom components

from gator.components.all import *
# Import your custom components
# To avoid import issues the import pattern should be the following:
# from .<customComponentModule> import <CustomComponentClass>
# Use the same pattern for non-component files aswell.

allComponents = [
    Transform,
    SpriteRenderer,
    # Add your components to this list
]
"""

EMPTY_PROJECT_CUSTOM_RES = """# Gator Engine Editor - Auto generated file - Modify loading custom resources

from gator.resources.texture import Texture
from gator.resources.assets import Assets

# User must use this constants as the might be modified at export time for them to work properly
PROJECT_PATH = "projects/<PROJECTNAME>/"
ASSETS_PATH = PROJECT_PATH+"assets/"
IMAGES_PATH = ASSETS_PATH+"images/"

def loadResources():
    # Resource loading example:
    # Assets.registerTexture("textureAssetName", IMAGES_PATH+"myImageName.png") \
            .registerTexture("anotherTextureAssetName", IMAGES_PATH+"mySecondImageName.png")
    pass
"""

EXPORT_TEMPLATE = """#########################################################################################################################################

# Gator Engine Editor - Auto generated file - Do not modify

# For this file or the built EXE to run the current working directory must be the directory this file is in.

# After this file is converted to an exe the following files can be deleted:
# - every python file / __pycache__ folder, including this file.
# - every *.geproject file.

# After this file is converted to an exe the following files must be kept in the folder with the same relative parenting:
# - the assets folder and its subfolders and files.
# - the libs folder and its subfolders and files.
# - the GatorEngine_<PROJECTNAME> folder, it's assets folder, subfolders and files, all *.ge files, all user-added folders and resources.

# The EXE must be placed in the same folder this python file is placed.

#########################################################################################################################################

# adding the GLFW libraries to the dll search path
import os
os.add_dll_directory(os.getcwd()+"/libs/GLFW")

# importing required gator engine classes
from gator.common.settings import AppSettings
from gator.application import Application

# importing user-customized required project files to avoid dynamic loading
from GatorEngine_<PROJECTNAME> import allComponents
from GatorEngine_<PROJECTNAME> import customResources

# main function
def main():
    # creating settings with information from the project settings
    settings = AppSettings(<WINWIDTH>, <WINHEIGHT>, <WINMAX>, "<WINTITLE>", "<SCENENAME>", "<PROJECTNAME>", "", allComponents, customResources)
    # creating the application
    app = Application()
    # passing the settings to the application
    app.init(settings)
    # running the application
    app.run()


# checking this file has been run
if __name__ == "__main__":
    # starting the game
    main()

"""
