import imgui
import os
import gator.common.gimgui as gimgui

class ProjectSettingsTab:
    def __init__(self, editor):
        self.editor = editor
        self.windowWidth = 1920
        self.windowHeight = 1080
        self.widthAuto = True
        self.heightAuto = True
        self.maximized = True
        self.windowTitle = "My Game"
        self.sceneName = "error"
        self.exportName = "MyGame"
        
    def toFile(self):
        return {
            "windowWidth": self.windowWidth,
            "windowHeight": self.windowHeight,
            "widthAuto": self.widthAuto,
            "heightAuto": self.heightAuto,
            "maximized": self.maximized,
            "windowTitle": self.windowTitle,
            "sceneName": self.sceneName,
            "exportName": self.exportName
        }
        
    def fromFile(self, data:dict):
        self.windowWidth = data["windowWidth"]
        self.windowHeight = data["windowHeight"]
        self.widthAuto = data["widthAuto"]
        self.heightAuto = data["heightAuto"]
        self.maximized = data["maximized"]
        self.windowTitle = data["windowTitle"]
        self.sceneName = data["sceneName"]
        self.exportName = data["exportName"]
        
    def getScenes(self):
        return [file.replace(".ge","") for file in os.listdir(f"projects/{self.editor.app.projectName}") if ".ge" in file]
        
    def imgui(self):
        scenes = self.getScenes()
        if self.sceneName not in scenes and len(scenes) > 0:
            self.sceneName = scenes[0]
            
        imgui.begin("Project Settings##ProjectSettingsTab")
        if len(scenes) <= 0:
            imgui.text("Error: At least one scene must exist to edit project settings")
            imgui.end()
            return
        
        _, self.sceneName = gimgui.enumDropdown("Main Scene", scenes, self.sceneName)
        _, exportName = gimgui.inputText("Export Name", self.exportName)
        if len(exportName) > 0:
            self.exportName = exportName
        _, self.windowTitle = gimgui.inputText("Window Title", self.windowTitle)
        _, self.windowWidth = gimgui.dragInt("Window Width", self.windowWidth)
        _, self.widthAuto = gimgui.checkbox("Auto Width", self.widthAuto)
        _, self.windowHeight = gimgui.dragInt("Window Height", self.windowHeight)
        _, self.heightAuto = gimgui.checkbox("Auto Height", self.heightAuto)
        _, self.maximized = gimgui.checkbox("Win Maximized", self.maximized)
        
        imgui.end()