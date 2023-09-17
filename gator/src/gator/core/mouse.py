import glfw
import glm
from typing import Generator, Any

from gator.common.singletons import Singletons


class Mouse:
    buttons = glfw
    anyButton: bool = False
    buttonsPressedCount: int = 0
    mousePos: glm.vec2 = glm.vec2()
    mouseRel: glm.vec2 = glm.vec2()
    scrollDelta: glm.vec2 = glm.vec2()
    maxButton: int = 29
    _mouseCache: dict[int, int] = {button: 0 for button in range(30)}
    _repeatCache: dict[int, int] = {button: 0 for button in range(30)}

    @classmethod
    def frameStart(cls):
        cls._mouseCache = {button: 0 for button in range(30)}
        cls.scrollDelta, cls.mouseRel = glm.vec2(), glm.vec2()

    @classmethod
    def mouseButtonCallback(cls, window: glfw._GLFWwindow, button: int, action: int, mods: int):
        if action == glfw.PRESS:
            cls._mouseCache[button] = action
            cls.buttonsPressedCount += 1
            cls._repeatCache[button] = action
        elif action == glfw.RELEASE:
            cls._mouseCache[button] = -1
            cls.buttonsPressedCount -= 1
            cls._repeatCache[button] = action
        cls.anyButton = cls.buttonsPressedCount > 0

    @classmethod
    def cursorPosCallback(cls, window: glfw._GLFWwindow, xpos: int, ypos: int):
        cls.mouseRel.x = xpos-cls.mousePos.x
        cls.mouseRel.y = ypos-cls.mousePos.y
        cls.mousePos.x, cls.mousePos.y = xpos, ypos

    @classmethod
    def scrollCallback(cls, window: glfw._GLFWwindow, xoffset: int, yoffset: int):
        cls.scrollDelta.x, cls.scrollDelta.y = xoffset, yoffset

    @classmethod
    def setPos(cls, x: int, y: int):
        glfw.set_cursor_pos(Singletons.app.window.glfwWindow, x, y)
        cls.cursorPosCallback(Singletons.app.window.glfwWindow, x, y)

    @classmethod
    def getButton(cls, button: int) -> bool:
        return cls._repeatCache[button] == glfw.PRESS

    @classmethod
    def getButtonDown(cls, button: int) -> bool:
        return cls._mouseCache[button] == glfw.PRESS

    @classmethod
    def getButtonUp(cls, button: int) -> bool:
        return cls._mouseCache[button] == -1

    @classmethod
    def getButtonIdle(cls, button: int) -> bool:
        return cls._mouseCache[button] == glfw.RELEASE

    @classmethod
    def getButtonRepeat(cls, button: int) -> bool:
        return cls._repeatCache[button] == glfw.PRESS and cls._mouseCache[button] != glfw.PRESS

    @classmethod
    def getButtonsPressed(cls) -> Generator[int, Any, Any]:
        for button, val in cls._repeatCache.items():
            if val == glfw.PRESS:
                yield button

    @classmethod
    def getDragging(cls, button: int) -> bool:
        return glm.length(cls.mouseRel) != 0 and cls._repeatCache[button] == glfw.PRESS and cls._mouseCache[button] != glfw.PRESS
