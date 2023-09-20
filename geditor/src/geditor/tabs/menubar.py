import imgui
from gator.common.singletons import Singletons
from gator.common.gimgui import Tracker

class MenuBarTab:
    def __init__(self, saveFunc, openFunc, exportFunc, quitFunc, createSceneFunc, loadSceneFunc):
        self.saveFunc = saveFunc
        self.openFunc = openFunc
        self.exportFunc = exportFunc
        self.quitFunc = quitFunc
        self.createSceneFunc = createSceneFunc
        self.loadSceneFunc = loadSceneFunc
        
        self.icSceneName: str = ""
        
    def imgui(self):
        if imgui.begin_main_menu_bar():
            Tracker.menuBarH = imgui.get_window_size()[1]
            if imgui.begin_menu("File"):
                if not Singletons.editor.playing and imgui.menu_item("Save")[0]:
                    self.saveFunc()
                if imgui.menu_item("Open")[0]:
                    self.openFunc()
                if imgui.menu_item("Export")[0]:
                    self.exportFunc()
                if imgui.menu_item("Quit")[0]:
                    self.quitFunc()
                imgui.end_menu()
            if imgui.begin_menu("Scene"):
                scenes = Singletons.editor.getScenes()
                for scene in scenes:
                    if imgui.menu_item(f"Load {scene}")[0]:
                        self.loadSceneFunc(scene)
                _, self.icSceneName = imgui.input_text("##SceneNameInput", self.icSceneName)
                self.icSceneName = self.icSceneName.replace(" ","").replace(".","").replace(":","")
                if self.icSceneName == "": self.icSceneName = "NewScene"
                if self.icSceneName in scenes: self.icSceneName = "NewScene"
                imgui.same_line()
                if imgui.button("Create Scene"):
                    self.createSceneFunc(self.icSceneName)
                imgui.text("To delete a scene delete the <name>.ge file")
                imgui.end_menu()
            
            imgui.end_main_menu_bar()