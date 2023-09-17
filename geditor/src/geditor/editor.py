import imgui
import glfw
import os
import json
import shutil

from gator.common.settings import AppSettings, EMPTY_PROJECT_MAIN_SCENE, EMPTY_PROJECT_COMPS_MODULE, EMPTY_PROJECT_CUSTOM_RES, EXPORT_TEMPLATE
from gator.common.singletons import Singletons
import gator.common.events as events

from geditor.imguilayer import ImguiLayer
from geditor.tabs.properties import PropertiesTab
from geditor.tabs.scenesettings import SceneSettingsTab
from geditor.tabs.menubar import MenuBarTab
from geditor.tabs.projectsettings import ProjectSettingsTab

from gator.core.time import Time
from gator.core.keys import Keyboard
from gator.core.mouse import Mouse

from gator.resources.assets import Assets
from gator.graphics.shader import Shader
from gator.application import Application


class GatorEditor:

    def __init__(self, appSettings: AppSettings):
        Singletons.editor = self
        events.register(events.SCENE_SAVED, self.whenSceneSave)
        events.register(events.SCENE_LOADED, self.whenSceneLoad)
        
        self.projectSettingsTab: ProjectSettingsTab = ProjectSettingsTab(self)
        
        self.app: Application = Application()
        self.app.init(appSettings)
        self.imguiLayer: ImguiLayer = ImguiLayer(
            self.app.window.width, self.app.window.height, self.app.window.glfwWindow, self.app.window)
        self.inProject: bool = not (
            appSettings.projectName == "none" and appSettings.sceneName == "idle")
        self.playing = False

        self.icProjectName: str = ""
        
        self.propertiesTab: PropertiesTab = PropertiesTab()
        self.sceneSettingsTab: SceneSettingsTab = SceneSettingsTab()
        self.menuBarTab: MenuBarTab = MenuBarTab(self.menuBarSave, self.menuBarOpen, self.menuBarExport, self.menuBarQuit, self)

        # e = self.app.scene.instantiate("TestObject", 0)
        # e.addComponent(SpriteRenderer(Sprite(Assets.getTexture("pygame")), Colors.CYAN))
        
    def whenSceneSave(self, event):
        with open(f"projects/{self.app.projectName}/settings.geproject", "w") as settingsFile:
            json.dump(self.projectSettingsTab.toFile(), settingsFile)
        
    def whenSceneLoad(self, event):
        if not os.path.exists(f"projects/{self.app.projectName}/settings.geproject"):
            with open(f"projects/{self.app.projectName}/settings.geproject", "w") as settingsFile:
                json.dump(self.projectSettingsTab.toFile(), settingsFile)
        with open(f"projects/{self.app.projectName}/settings.geproject", "r") as settingsFile:
            self.projectSettingsTab.fromFile(json.load(settingsFile))
        
    def menuBarSave(self):
        if not self.playing:
            self.app.scene.save()
            
    def menuBarOpen(self):
        self.openProject("none")
        self.inProject = False
        self.icProjectName = ""
        
    def menuBarExport(self):
        self.app.scene.save()
        exportContent = EXPORT_TEMPLATE \
            .replace("<WINWIDTH>", '"auto"' if self.projectSettingsTab.widthAuto else str(self.projectSettingsTab.windowWidth))  \
            .replace("<WINHEIGHT>", '"auto"' if self.projectSettingsTab.heightAuto else str(self.projectSettingsTab.windowHeight)) \
            .replace("<WINTITLE>", self.projectSettingsTab.windowTitle) \
            .replace("<WINMAX>", "True" if self.projectSettingsTab.maximized else "False") \
            .replace("<SCENENAME>", self.projectSettingsTab.sceneName) \
            .replace("<PROJECTNAME>", self.app.projectName.replace("GatorEngine_",""))
        with open(f"projects/{self.app.projectName}/exports/{self.projectSettingsTab.exportName}.py", "w") as exportFile:
            exportFile.write(exportContent)
        os.mkdir(f"projects/{self.app.projectName}/exports/{self.app.projectName}")
        for dirname, subdirs, files in os.walk(f"projects/{self.app.projectName}"):
            try:
                if dirname == "exports": continue
                for subdir in subdirs:
                    if subdir == "exports":
                        continue
                    os.mkdir(f"projects/{self.app.projectName}/exports/{dirname.replace('projects/','')}/{subdir}")
                for file in files:
                    shutil.copy(f"{dirname}/{file}", f"projects/{self.app.projectName}/exports/{dirname.replace('projects/','')}/{file}")
            except Exception as e:
                print(e)
        content = None
        with open(f"projects/{self.app.projectName}/exports/{self.app.projectName}/customResources.py", "r") as customResFile:
            content = customResFile.read().replace("projects/","")
        if content is not None:
            with open(f"projects/{self.app.projectName}/exports/{self.app.projectName}/customResources.py", "w") as customResFile:
                customResFile.write(content)
        shutil.copytree("assets", f"projects/{self.app.projectName}/exports/assets")
        shutil.copytree("libs", f"projects/{self.app.projectName}/exports/libs")
            
    def menuBarQuit(self):
        glfw.set_window_should_close(self.app.window.glfwWindow, True)

    def update(self, shader: Shader):
        self.app.scene.update()
        self.app.scene.editorUpdate()
        self.app.scene.render(shader)
        self.imguiLayer.imgui(self.propertiesTab.imgui,
                              self.sceneSettingsTab.imgui,
                              self.menuBarTab.imgui,
                              self.projectSettingsTab.imgui)

    def projectSelection(self):
        imgui.begin("Open Project##OpenProjectWindow")

        _, self.icProjectName = imgui.input_text(
            "##projectname", self.icProjectName)
        self.icProjectName = self.icProjectName.replace(" ","").replace(":","").replace(".","")
        if self.icProjectName == "none":
            self.icProjectName = "NewProject"
        imgui.same_line()
        if imgui.button("Open Project"):
            if os.path.exists(f"projects/GatorEngine_{self.icProjectName}"):
                self.openProject("GatorEngine_"+self.icProjectName)
            else:
                self.createProject("GatorEngine_"+self.icProjectName)

        imgui.end()

    def openProject(self, name: str):
        self.app.projectName = f"{name}"
        if not os.path.exists(f"projects/{name}/allComponents.py"):
            with open(f"projects/{name}/allComponents.py", "w") as allCompsFile:
                allCompsFile.write(EMPTY_PROJECT_COMPS_MODULE)
        if not os.path.exists(f"projects/{name}/customResources.py"):
            with open(f"projects/{name}/customResources.py", "w") as customResFile:
                customResFile.write(EMPTY_PROJECT_CUSTOM_RES.replace("<PROJECTNAME>", name))
        if not os.path.exists(f"projects/{name}/settings.geproject"):
            with open(f"projects/{name}/settings.geproject", "w") as settingsFile:
                json.dump(self.projectSettingsTab.toFile(), settingsFile)
        if not os.path.exists(f"projects/{name}/assets"):
            os.mkdir(f"projects/{name}/assets")
        if not os.path.exists(f"projects/{name}/assets/images"):
            os.mkdir(f"projects/{name}/assets/images")
        if not os.path.exists(f"projects/{name}/exports"):
            os.mkdir(f"projects/{name}/exports")
        files = os.listdir(f"projects/{name}")
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
            with open(f"projects/{name}/main.ge", "w") as mainSceneFile:
                mainSceneFile.write(EMPTY_PROJECT_MAIN_SCENE)
                self.app.changeScene("main")
                found = True
        self.inProject = True

    def createProject(self, name: str):
        os.mkdir(f"projects/{name}")
        os.mkdir(f"projects/{name}/assets")
        os.mkdir(f"projects/{name}/assets/images")
        os.mkdir(f"projects/{name}/exports")
        self.app.projectName = f"{name}"
        with open(f"projects/{name}/allComponents.py", "w") as allCompsFile:
            allCompsFile.write(EMPTY_PROJECT_COMPS_MODULE)
        with open(f"projects/{name}/main.ge", "w") as mainSceneFile:
            mainSceneFile.write(EMPTY_PROJECT_MAIN_SCENE)
        with open(f"projects/{name}/customResources.py", "w") as customResFile:
            customResFile.write(EMPTY_PROJECT_CUSTOM_RES.replace("<PROJECTNAME>", name))
        with open(f"projects/{name}/settings.geproject", "w") as settingsFile:
            json.dump(self.projectSettingsTab.toFile(), settingsFile)
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

        self.destroy()

    def destroy(self):
        self.imguiLayer.destroy()
        self.app.destroy()
