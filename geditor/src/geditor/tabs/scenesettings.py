import imgui

import gator.common.gimgui as gimgui
from gator.common.singletons import Singletons


class SceneSettingsTab:
        
    def imgui(self):
        imgui.begin("Scene Settings##SceneSettingsTabWindow")
        _, Singletons.app.scene.clearColor = gimgui.colorEdit4("Scene Color", Singletons.app.scene.clearColor)
        _, Singletons.app.scene.camera.position = gimgui.dragVec3("Camera Pos", Singletons.app.scene.camera.position)
        _, Singletons.app.scene.camera.zoom = gimgui.dragFloat("Camera Zoom", Singletons.app.scene.camera.zoom, 0.01)
        imgui.end()