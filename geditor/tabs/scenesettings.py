import imgui

import common.gimgui as gimgui
from common.singletons import Singletons


class SceneSettingsTab:
        
    def imgui(self):
        imgui.begin("Scene Settings##SceneSettingsTabWindow")
        _, Singletons.app.scene.clearColor = gimgui.colorEdit4("Scene Color", Singletons.app.scene.clearColor)
        _, Singletons.app.scene.camera.position = gimgui.dragVec3("Camera Pos", Singletons.app.scene.camera.position)
        imgui.end()