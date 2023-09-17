import imgui
import os

from common.settings import AppSettings, EMPTY_PROJECT_MAIN_SCENE, EMPTY_PROJECT_COMPS_MODULE
from common.singletons import Singletons

from geditor.imguilayer import ImguiLayer
from geditor.tabs.properties import PropertiesTab
from geditor.tabs.scenesettings import SceneSettingsTab

from gator.core.time import Time
from gator.core.keys import Keyboard
from gator.core.mouse import Mouse

from gator.resources.assets import Assets
from gator.graphics.shader import Shader
from gator.application import Application


class GatorEditor:

    def __init__(self, appSettings: AppSettings):
        Singletons.editor = self
        self.app: Application = Application()
        self.app.init(appSettings)
        self.imguiLayer: ImguiLayer = ImguiLayer(
            self.app.window.width, self.app.window.height, self.app.window.glfwWindow, self.app.window)
        self.inProject: bool = not (
            appSettings.projectName == "none" and appSettings.sceneName == "idle")

        self.icProjectName: str = ""

        self.propertiesTab: PropertiesTab = PropertiesTab()
        self.sceneSettingsTab: SceneSettingsTab = SceneSettingsTab()

        # e = self.app.scene.instantiate("TestObject", 0)
        # e.addComponent(SpriteRenderer(Sprite(Assets.getTexture("pygame")), Colors.CYAN))

    def update(self, shader: Shader):
        self.app.scene.update()
        self.app.scene.editorUpdate()
        self.app.scene.render(shader)
        self.imguiLayer.imgui(self.propertiesTab.imgui,
                              self.sceneSettingsTab.imgui)

    def projectSelection(self):
        imgui.begin("Open Project##OpenProjectWindow")

        changed, self.icProjectName = imgui.input_text(
            "##projectname", self.icProjectName)
        imgui.same_line()
        if imgui.button("Open Project"):
            if os.path.exists(f"geditor/projects/{self.icProjectName}"):
                self.openProject(self.icProjectName)
            else:
                self.createProject(self.icProjectName)

        imgui.end()

    def openProject(self, name: str):
        self.app.projectName = f"{name}"
        if not os.path.exists(f"geditor/projects/{name}/allComponents.py"):
            with open(f"geditor/projects/{name}/allComponents.py", "w") as allCompsFile:
                allCompsFile.write(EMPTY_PROJECT_COMPS_MODULE)
        files = os.listdir(f"geditor/projects/{name}")
        found = False
        for file in files:
            if file == "main.ge":
                self.app.changeScene("main")
                found = True
        if not found:
            for file in files:
                if ".ge" in file:
                    self.app.changeScene(f"{file.replace('.ge','')}")
                    found = True
        if not found:
            with open(f"geditor/projects/{name}/main.ge", "w") as mainSceneFile:
                mainSceneFile.write(EMPTY_PROJECT_MAIN_SCENE)
                self.app.changeScene("main")
                found = True
        self.inProject = True

    def createProject(self, name: str):
        os.mkdir(f"geditor/projects/{name}")
        self.app.projectName = f"{name}"
        with open(f"geditor/projects/{name}/allComponents.py", "w") as allCompsFile:
            allCompsFile.write(EMPTY_PROJECT_COMPS_MODULE)
        with open(f"geditor/projects/{name}/main.ge", "w") as mainSceneFile:
            mainSceneFile.write(EMPTY_PROJECT_MAIN_SCENE)
        self.app.changeScene("main")
        self.inProject = True

    def run(self):
        beginTime = Time.getTime()
        endTime = Time.getTime()
        spriteShader = Assets.getShader("sprite")

        while not self.app.window.shouldClose:
            self.app.window.clear(self.app.scene.clearColor)
            Keyboard.frameStart()
            Mouse.frameStart()
            self.app.window.pollEvents()
            self.imguiLayer.frameStart()

            if self.inProject:
                self.update(spriteShader)
            else:
                self.projectSelection()

            self.imguiLayer.frameEnd()
            self.app.window.swapBuffers()
            endTime = Time.getTime()
            Time.dt = (endTime-beginTime)*Time.scale
            beginTime = endTime

            self.app.window.title = f"Gator Engine Editor [Test] ({Time.getFPS():.0f} FPS)"

        self.app.scene.save()
        self.destroy()

    def destroy(self):
        self.app.destroy()
