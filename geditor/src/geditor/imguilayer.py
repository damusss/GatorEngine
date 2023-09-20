import imgui
from glfw import _GLFWwindow
from imgui.integrations import glfw as imgui_glfw

from gator.core.keys import Keyboard
from gator.core.mouse import Mouse
from gator.core.time import Time
from gator.core.window import Window

import gator.common.gimgui as gimgui
from gator.common.singletons import Singletons


class ImguiLayer:
    def __init__(self, width: int, height: int, glfwWindow: _GLFWwindow, window: Window):
        self.ctx = imgui.create_context()
        self.io = imgui.get_io()
        self.io.display_size = width, height
        self.io.fonts.get_tex_data_as_rgba32()
        self.editorMainFont = self.io.fonts.add_font_from_file_ttf(
            "assets/fonts/editor-main.ttf", 20,
        )
        self.renderer = imgui_glfw.GlfwRenderer(
            glfwWindow, True, Keyboard.keyCallback, Mouse.cursorPosCallback, window.windowSizeCallback, Mouse.scrollCallback)
    
    def destroy(self):
        self.renderer.shutdown()
        
    def docking(self):
        windowFlags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING

        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(Singletons.app.window._width, Singletons.app.window._height)
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
        windowFlags = windowFlags | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | \
                imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | \
                imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS

        imgui.begin("Gator Editor Dockspace", True, windowFlags)
        imgui.pop_style_var(2)

        imgui.dockspace(imgui.get_id("GatorEditorDockspace"), (Singletons.app.window._width, Singletons.app.window._height))

        imgui.end()

    def frameStart(self):
        gimgui.Tracker.stolenPopup = False
        imgui.new_frame()
        self.renderer.process_inputs(Time.dt)
        imgui.push_font(self.editorMainFont)
        #imgui.dockspace(666, (Singletons.app.window._width, Singletons.app.window._height))
        #self.docking()

    def imgui(self, *imgui_tabs):
        [tab.imgui() for tab in imgui_tabs]

    def frameEnd(self):
        
        imgui.pop_font()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
        imgui.end_frame()
