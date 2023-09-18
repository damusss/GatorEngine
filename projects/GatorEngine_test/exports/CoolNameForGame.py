#########################################################################################################################################
# Gator Engine Editor - Auto generated file - Do not modify

# For this file or the built EXE to run the current working directory must be the directory this file is in.

# After this file is converted to an exe the following files can be deleted:
# - every python file / __pycache__ folder, including this file.
# - every *.geproject file.

# After this file is converted to an exe the following files must be kept in the folder with the same relative parenting:
# - the assets folder and its subfolders and files.
# - the libs folder and its subfolders and files.
# - the GatorEngine_test folder, it's assets folder, subfolders and files, all *.ge files, all user-added folders and resources.

# The EXE must be placed in the same folder this python file is placed.

#########################################################################################################################################

# adding the GLFW libraries to the dll search path
import os
os.add_dll_directory(os.getcwd()+"/libs/GLFW")

# importing required gator engine classes
from gator.common.settings import AppSettings
from gator.application import Application

# importing user-customized required project files to avoid dynamic loading
from GatorEngine_test import allComponents
from GatorEngine_test import customResources

# main function
def main():
    # creating settings with information from the project settings
    settings = AppSettings("auto", "auto", True, "My Game", "main", "test", "", allComponents, customResources)
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

