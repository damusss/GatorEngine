import imgui

import gator.common.gimgui as gimgui
from gator.common.singletons import Singletons
from gator.common.settings import WINDOW_FLAGS, COLUMN_DIVIDER, HEIGHT_DIVIDER
from gator.common.gimgui import Tracker


class SceneSettingsTab:
        
    def imgui(self):
        imgui.set_next_window_position(Singletons.app.window._width//COLUMN_DIVIDER, Tracker.menuBarH)
        imgui.set_next_window_size((Singletons.app.window._width-(Singletons.app.window._width//COLUMN_DIVIDER))//2,
                                   Singletons.app.window._height//HEIGHT_DIVIDER)
        imgui.begin("Scene Settings##SceneSettingsTabWindow", False, WINDOW_FLAGS)
        _, Singletons.app.scene.clearColor = gimgui.colorEdit4("Scene Color", Singletons.app.scene.clearColor)
        _, Singletons.app.scene.camera.position = gimgui.dragVec3("Camera Pos", Singletons.app.scene.camera.position)
        _, Singletons.app.scene.camera.zoom = gimgui.dragFloat("Camera Zoom", Singletons.app.scene.camera.zoom, 0.01)
        imgui.end()