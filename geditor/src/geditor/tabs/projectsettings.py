import imgui
import os
import gator.common.gimgui as gimgui
from gator.common.singletons import Singletons

class ProjectSettingsTab:
    def __init__(self):
        self.windowWidth: int = 1920
        self.windowHeight: int = 1080
        self.widthAuto: bool = True
        self.heightAuto: bool = True
        self.maximized: bool = True
        self.windowTitle: str = "My Game"
        self.sceneName: str = "error"
        self.exportName: str = "MyGame"
        
    def toFile(self) -> dict[str, str|int|bool]:
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
        
    def fromFile(self, data: dict[str, str|int|bool]):
        self.windowWidth = data["windowWidth"]
        self.windowHeight = data["windowHeight"]
        self.widthAuto = data["widthAuto"]
        self.heightAuto = data["heightAuto"]
        self.maximized = data["maximized"]
        self.windowTitle = data["windowTitle"]
        self.sceneName = data["sceneName"]
        self.exportName = data["exportName"]
        
        
    def imgui(self):
        scenes = Singletons.editor.getScenes()
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