from OpenGL.GL import *

from common.singletons import Singletons
from common.settings import AppSettings

from gator.core.window import Window
from gator.core.time import Time
from gator.core.keys import Keyboard
from gator.core.mouse import Mouse

from gator.resources.assets import Assets
from gator.scene import Scene


class Application:

    def init(self, appSettings: AppSettings):
        Singletons.app = self
        self.projectName = appSettings.projectName
        self.window = Window(
            appSettings.width, appSettings.height, appSettings.title)
        Assets.preRegister()

        self.scene = Scene(appSettings.sceneName)
        self.scene.load()

    def changeScene(self, name: str):
        if self.scene is not None:
            self.scene.destroy()
        self.scene = Scene(name)
        self.scene.load()

    def run(self):
        beginTime = Time.getTime()
        endTime = Time.getTime()
        spriteShader = Assets.getShader("sprite")

        while not self.window.shouldClose:
            self.window.clear(self.scene.clearColor)
            Keyboard.frameStart()
            Mouse.frameStart()
            self.window.pollEvents()

            self.scene.update()
            self.scene.render(spriteShader)

            self.window.swapBuffers()
            endTime = Time.getTime()
            Time.dt = (endTime-beginTime)*Time.scale
            beginTime = endTime

        self.destroy()

    def destroy(self):
        self.scene.destroy()
        Assets.destroy()
        self.window.destroy()
