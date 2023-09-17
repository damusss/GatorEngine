import glfw
from typing import Generator, Any

from common.singletons import Singletons


class Keyboard:
    keys = glfw
    anyKey: bool = False
    keysPressedCount: int = 0
    maxKey: int = 349
    _keyCache: dict[int, int] = {key: 0 for key in range(350)}

    @classmethod
    def frameStart(cls):
        cls._keyCache = {key: 0 for key in range(350)}

    @classmethod
    def keyCallback(cls, window: glfw._GLFWwindow, key: int, scancode: int, action: int, mods: int):
        cls._keyCache[key] = action
        if action == glfw.RELEASE:
            cls.keysPressedCount -= 1
            cls._keyCache[key] = -1
        elif action == glfw.PRESS:
            cls.keysPressedCount += 1
        cls.anyKey = cls.keysPressedCount > 0

    @classmethod
    def getClipboard(cls) -> str:
        return glfw.get_clipboard_string(Singletons.app.window.glfwWindow)

    @classmethod
    def setClipboard(cls, text: str):
        glfw.set_clipboard_string(Singletons.app.window.glfwWindow, text)

    @classmethod
    def getKey(cls, key: int) -> bool:
        return cls._keyCache[key] == glfw.PRESS or cls._keyCache[key] == glfw.REPEAT

    @classmethod
    def getKeyDown(cls, key: int) -> bool:
        return cls._keyCache[key] == glfw.PRESS

    @classmethod
    def getKeyUp(cls, key: int) -> bool:
        return cls._keyCache[key] == -1

    @classmethod
    def getKeyRepeat(cls, key: int) -> bool:
        return cls._keyCache[key] == glfw.REPEAT

    @classmethod
    def getKeyIdle(cls, key: int) -> bool:
        return cls._keyCache[key] == glfw.RELEASE

    @classmethod
    def getKeysPressed(cls) -> Generator[int, Any, Any]:
        for key, val in cls._keyCache.items():
            if val > 0:
                yield key
