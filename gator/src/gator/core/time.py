import pyglfw.pyglfw as glfw


class Time:
    dt: float = 0
    scale: float = 1

    @staticmethod
    def getTime() -> float:
        return glfw.get_time()

    @classmethod
    def getFPS(cls) -> float:
        return 1/cls.dt
