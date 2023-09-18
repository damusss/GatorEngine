import imgui
from gator.common.singletons import Singletons

class MenuBarTab:
    def __init__(self, saveFunc, openFunc, exportFunc, quitFunc, playFunc, stopFunc):
        self.saveFunc = saveFunc
        self.openFunc = openFunc
        self.exportFunc = exportFunc
        self.quitFunc = quitFunc
        self.playFunc = playFunc
        self.stopFunc = stopFunc
        
    def imgui(self):
        if imgui.begin_main_menu_bar():
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
            if imgui.button("Play"):
                self.playFunc()
            if imgui.button("Stop"):
                self.stopFunc()
            imgui.end_main_menu_bar()