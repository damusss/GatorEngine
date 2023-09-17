import glfw
import glm
from OpenGL.GL import *

import gator.common.error as error
from gator.core.keys import Keyboard
from gator.core.mouse import Mouse


class Window:
    def __init__(self, width: int | str, height: int | str, title: str, maximized):
        if not glfw.init():
            error.fatal(error.GLFWError, "GLFW initialization failed")

        mainMonitor = glfw.get_primary_monitor()
        videoMode = glfw.get_video_modes(mainMonitor)[-1]

        if width == "auto":
            width = videoMode.size.width
        if width == "half":
            width = videoMode.size.width//2
        if height == "auto":
            height = videoMode.size.height
        if height == "half":
            height = videoMode.size.height//2

        if maximized:
            glfw.window_hint(glfw.MAXIMIZED, True)
        self.glfwWindow: int = glfw.create_window(
            width, height, title, None, None)
        glfw.make_context_current(self.glfwWindow)
        glfw.swap_interval(0)

        self._width: int = width
        self._title: str = title
        self._height: int = height

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_TEXTURE_2D)

        glfw.set_cursor_pos_callback(self.glfwWindow, Mouse.cursorPosCallback)
        glfw.set_key_callback(self.glfwWindow, Keyboard.keyCallback)
        glfw.set_window_size_callback(self.glfwWindow, self.windowSizeCallback)
        glfw.set_mouse_button_callback(
            self.glfwWindow, Mouse.mouseButtonCallback)
        glfw.set_scroll_callback(self.glfwWindow, Mouse.scrollCallback)

    def windowSizeCallback(self, window: glfw._GLFWwindow, width: int, height: int):
        self._width, self._height = width, height

    def destroy(self):
        glfw.terminate()

    def clear(self, color: glm.vec4):
        glClearColor(color.x, color.y, color.z, color.w)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def pollEvents(self):
        glfw.poll_events()

    def swapBuffers(self):
        glfw.swap_buffers(self.glfwWindow)

    @property
    def shouldClose(self) -> bool:
        return glfw.window_should_close(self.glfwWindow)

    @property
    def width(self) -> int: return self._width

    @width.setter
    def width(self, val: int):
        glfw.set_window_size(self.glfwWindow, val, self._height)
        self._width = val

    @property
    def height(self) -> int: return self._height

    @height.setter
    def height(self, val: int):
        glfw.set_window_size(self.glfwWindow, self._width, val)
        self._height = val

    @property
    def size(self) -> tuple[int, int]: return (self._width, self._height)

    @size.setter
    def size(self, val: tuple[int, int]):
        self.width = val[0]
        self.height = val[1]

    @property
    def title(self) -> str: return self._title

    @title.setter
    def title(self, val: str):
        glfw.set_window_title(self.glfwWindow, val)
        self._title = val
