import imgui

from gator.components.component import Component
from gator.components.transform import Transform

from gator.common.singletons import Singletons
import gator.common.events as events
import gator.common.gimgui as gimgui
import gator.common.error as error

from gator.graphics.renderbatch import RenderBatch


class Entity:
    GLOBAL_ID: int = 0

    def __init__(self, name: str, layer: int, id=None):
        self.ID: int = Entity.GLOBAL_ID if not id else id
        if not id:
            Entity.GLOBAL_ID += 1
        self.name: str = name
        self.layer: int = layer
        self.dead: bool = False
        self.scene = Singletons.app.scene
        self.dirty: bool = True
        self.components: dict[type[Component], Component] = {}
        self.transform: Transform = None
        self._renderbatch: RenderBatch = None
        self._batchindex: int = -1
        self._lastLayer = self.layer
        Singletons.app.scene._entityUIDCache[self.ID] = self
        Singletons.app.scene._refreshLayerCache()

    def toFile(self) -> dict:
        return {
            "id": self.ID,
            "name": self.name,
            "layer": self.layer,
            "components": [
                comp.toFile() for comp in self.components.values()
            ]
        }

    @classmethod
    def fromFile(cls, eData: dict, allComps: list[type[Component]]):
        entity = Entity(eData["name"], eData["layer"], eData["id"])
        for cData in eData["components"]:
            for compType in allComps:
                if compType.__name__ == cData["type"]:
                    try:
                        comp = compType.fromFile(cData, entity)
                    except Exception as e:
                        error.warning(error.GatorError, f"Could not load component '{eData['name']}:{compType.__name__}' from scene file '{Singletons.app.projectName}:{Singletons.app.scene.name}.ge'. The component will be skipped. Error details:\n{e}")
                        break
                    else:
                        entity.addComponent(comp)
                        if compType.__name__ == "Transform":
                            entity.transform = comp
        return entity

    def addComponent(self, component: Component) -> Component:
        self.components[component.__class__] = component
        component.entity = self
        component.init()
        if Singletons.app.scene.started:
            component.start()
        events.invoke(events.COMP_ADDED, component=component)
        self.dirty = True
        return component

    def getComponent(self, type: type[Component], default=None) -> Component:
        return self.components.get(type, default)

    def hasComponent(self, type: type[Component]) -> bool:
        return type in self.components

    def update(self):
        compsToRemove: list[list[type[Component], Component]] = []
        for name, comp in self.components.items():
            if comp.dead:
                compsToRemove.append([name, comp])
            if comp.active:
                comp.update()
        for name, comp in compsToRemove:
            if (name is Transform):
                continue
            comp.onDestroy()
            events.invoke(events.COMP_REMOVED, component=comp)
            self.components.pop(name)

    def editorUpdate(self):
        compsToRemove: list[list[type[Component], Component]] = []
        for name, comp in self.components.items():
            if comp.dead:
                compsToRemove.append([name, comp])
            if comp.active:
                comp.editorUpdate()
        for name, comp in compsToRemove:
            if (name is Transform):
                continue
            comp.onDestroy()
            events.invoke(events.COMP_REMOVED, component=comp)
            self.components.pop(name)

    def imgui(self):
        imgui.push_id(f"{self.ID}")
        imgui.text(f"UID: {self.ID}")
        _, self.name = gimgui.inputText("Name", self.name)
        _, self.layer = gimgui.inputInt("Layer", self.layer)
        changed, newActive = gimgui.checkbox("Active", self.active)
        if changed:
            self.active = newActive
        for comp in self.components.values():
            imgui.push_id(f"{comp.ID}")
            if imgui.collapsing_header(f"{comp.__class__.__name__}")[0]:
                comp.imgui()
            imgui.pop_id()
        if not gimgui.Tracker.stolenPopup and imgui.begin_popup_context_window("Entity Options"):
            if imgui.menu_item("Delete Entity")[0]:
                self.kill()
            elif imgui.menu_item("Duplicate Entity")[0]:
                Singletons.app.scene.duplicate(self)
            myCompStrs = [
                compType.__class__.__name__ for compType in self.components.values()]
            strToComps = {
                compType.__name__: compType for compType in Singletons.app.scene.allComponents if compType.__name__ not in myCompStrs}
            for compName, compType in strToComps.items():
                if imgui.menu_item(f"Add {compName}")[0]:
                    self.addComponent(compType())
            imgui.end_popup()
        imgui.pop_id()

    def start(self):
        for comp in self.components.values():
            comp.start()

    def onDestroy(self):
        for comp in self.components.values():
            comp.onDestroy()

    def kill(self):
        self.dead = True
        Singletons.app.scene._refreshLayerCache()
        if self in self.scene.inactiveEntities:
            self.scene.inactiveEntities.remove(self)
            self.scene.entities.append(self)

    def setDirty(self):
        self.dirty = True

    def setClean(self):
        self.dirty = False

    @property
    def active(self) -> bool:
        return self not in self.scene.inactiveEntities

    @active.setter
    def active(self, value: bool):
        if value:
            if self in self.scene.inactiveEntities:
                self.scene.inactiveEntities.remove(self)
                self.scene.entities.append(self)
                for comp in self.components.values():
                    Singletons.app.scene.renderer.addComponent(comp)
                    Singletons.app.scene.customRenderer.addComponent(comp)
        else:
            if self in self.scene.entities:
                self.scene.entities.remove(self)
                self.scene.inactiveEntities.append(self)
                for comp in self.components.values():
                    Singletons.app.scene.renderer.removeComponent(comp)
                    Singletons.app.scene.customRenderer.removeComponent(comp)
                self.dirty = True
