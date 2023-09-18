import imgui
from glfw import _GLFWwindow
from imgui.integrations import glfw as imgui_glfw

from gator.core.keys import Keyboard
from gator.core.mouse import Mouse
from gator.core.time import Time
from gator.core.window import Window

import gator.common.gimgui as gimgui


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

    def frameStart(self):
        gimgui.Tracker.stolenPopup = False
        imgui.new_frame()
        self.renderer.process_inputs(Time.dt)
        imgui.push_font(self.editorMainFont)

    def imgui(self, *imgui_tabs):
        [tab.imgui() for tab in imgui_tabs]

    def frameEnd(self):
        imgui.pop_font()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
        imgui.end_frame()
