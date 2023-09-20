import json
import glm
import importlib

from gator.core.camera import Camera
from gator.graphics.renderer import Renderer
from gator.graphics.customrenderer import CustomRenderer
from gator.graphics.shader import Shader
from gator.entity import Entity

from gator.components.transform import Transform
from gator.components.component import Component
from gator.components.all import defaultComponents

import gator.common.events as events
import gator.common.saving as saving
from gator.common.colors import Colors
from gator.common.singletons import Singletons


class Scene:
    def __init__(self, name: str):
        self.name: str = name
        self.camera: Camera = Camera()
        self.renderer: Renderer = Renderer()
        self.customRenderer: CustomRenderer = CustomRenderer()
        self.entities: list[Entity] = []
        self.inactiveEntities: list[Entity] = []
        self.started: bool = False
        self.clearColor = Colors.BLACK
        self.allComponents: list[type[Component]] = defaultComponents
        self._entityNameCache: dict[str, Entity] = {}
        self._entityUIDCache: dict[int, Entity] = {}
        self._entityLayerCache: dict[int, list[Entity]] = {}

    def load(self):
        self.entities = []
        self.inactiveEntities = []
        self._entityNameCache = {}
        self._entityUIDCache = {}
        self._entityLayerCache = {}
        for batch in self.renderer.batches:
            batch.reset()
        for batch in self.customRenderer.batches:
            batch.reset()
        with open(f"{Singletons.app.searchPath.replace('.','/')}{Singletons.app.projectName}/{self.name}.ge", "r") as saveFile:
            data = json.load(saveFile)
            self.camera.position = saving.loadVec3(data["camera"]["pos"])
            self.camera.zoom = data["camera"]["zoom"]
            self.clearColor = saving.loadVec4(data["clearColor"])
            self.allComponents = importlib.import_module(
                f"{Singletons.app.searchPath}{Singletons.app.projectName}.allComponents").allComponents if Singletons.app.modules["comps"] is None else Singletons.app.modules["comps"].allComponents
            importlib.import_module(
                f"{Singletons.app.searchPath}{Singletons.app.projectName}.customResources").loadResources() if Singletons.app.modules["res"] is None else Singletons.app.modules["res"].loadResources()
            for eData in data["entities"]:
                entity = Entity.fromFile(eData, self.allComponents)
                self.entities.append(entity)
                self._entityNameCache[entity.name] = entity
                self._entityUIDCache[entity.ID] = entity
                events.invoke(events.ENTITY_CREATED, entity=entity)
            for eData in data["inactiveEntities"]:
                entity = Entity.fromFile(eData, self.allComponents)
                self.entities.append(entity)
                entity.active = False
                self._entityNameCache[entity.name] = entity
                self._entityUIDCache[entity.ID] = entity
                events.invoke(events.ENTITY_CREATED, entity=entity)
            beid = -1
            bcid = -1
            for e in self.entities:
                if e.ID > beid:
                    beid = e.ID
                for c in e.components.values():
                    if c.ID > bcid:
                        bcid = c.ID
            for e in self.inactiveEntities:
                if e.ID > beid:
                    beid = e.ID
                for c in e.components.values():
                    if c.ID > bcid:
                        bcid = c.ID
            Entity.GLOBAL_ID = beid+1
            Component.GLOBAL_ID = bcid+1
            events.invoke(events.SCENE_LOADED)

    def save(self):
        saveData = {
            "entities": [entity.toFile() for entity in self.entities],
            "inactiveEntities": [entity.toFile() for entity in self.inactiveEntities],
            "camera": {
                "pos": saving.saveVec3(glm.vec3()),
                "zoom": 1
            },
            "clearColor": saving.saveVec4(self.clearColor)
        }
        with open(f"{Singletons.app.searchPath.replace('.','/')}{Singletons.app.projectName}/{self.name}.ge", "w") as saveFile:
            json.dump(saveData, saveFile)
            events.invoke(events.SCENE_SAVED)

    def start(self):
        self.started = True
        for entity in self.entities:
            entity.start()

    def update(self):
        entitiesToRemove: list[Entity] = []
        for entity in self.entities:
            if entity.dead:
                entitiesToRemove.append(entity)
                continue
            entity.update()
            self._entityNameCache[entity.name] = entity
        for entity in entitiesToRemove:
            entity.onDestroy()
            for comp in entity.components.values():
                events.invoke(events.COMP_REMOVED, component=comp)
            self.entities.remove(entity)
            if entity.name in self._entityNameCache:
                del self._entityNameCache[entity.name]
            if entity.ID in self._entityUIDCache:
                del self._entityUIDCache[entity.ID]
            events.invoke(events.ENTITY_KILLED, entity=entity)
            self._refreshLayerCache()
        self.camera.update()

    def editorUpdate(self):
        entitiesToRemove: list[Entity] = []
        for entity in self.entities:
            if entity.dead:
                entitiesToRemove.append(entity)
                continue
            entity.editorUpdate()
            self._entityNameCache[entity.name] = entity
        for entity in entitiesToRemove:
            entity.onDestroy()
            for comp in entity.components.values():
                events.invoke(events.COMP_REMOVED, component=comp)
            self.entities.remove(entity)
            if entity.name in self._entityNameCache:
                del self._entityNameCache[entity.name]
            if entity.ID in self._entityUIDCache:
                del self._entityUIDCache[entity.ID]
            events.invoke(events.ENTITY_KILLED, entity=entity)
            self._refreshLayerCache()
        self.camera.update()

    def render(self, shader: Shader):
        self.renderer.render(shader)
        self.customRenderer.render()

    def destroy(self):
        self.renderer.destroy()
        self.customRenderer.destroy()
        for entity in self.entities:
            entity.onDestroy()

    def instantiate(self, name: str, layer: int) -> Entity:
        entity = Entity(name, layer)
        t = entity.addComponent(Transform())
        entity.transform = t
        if self.started:
            entity.start()
        self.entities.append(entity)
        events.invoke(events.ENTITY_CREATED, entity=entity)
        return entity

    def duplicate(self, entity: Entity) -> Entity:
        fileEntity = entity.toFile()
        newEntity = Entity.fromFile(fileEntity, self.allComponents)
        newEntity.ID = Entity.GLOBAL_ID
        Entity.GLOBAL_ID += 1
        newEntity.transform.position.x += 0.5
        newEntity.transform.position.y += 0.5
        for comp in newEntity.components.values():
            comp.ID = Component.GLOBAL_ID
            Component.GLOBAL_ID += 1
        if entity.active:
            self.entities.append(newEntity)
        else:
            self.inactiveEntities.append(newEntity)
        events.invoke(events.ENTITY_CREATED, entity=entity)
        return newEntity

    def getEntityByID(self, ID: int) -> Entity | None:
        if ID in self._entityUIDCache:
            return self._entityUIDCache[ID]
        for entity in self.entities:
            if entity.ID == ID and not entity.dead:
                self._entityUIDCache[ID] = entity
                return entity
        return None

    def getEntityByName(self, name: str) -> Entity | None:
        if name in self._entityNameCache:
            return self._entityNameCache[name]
        for entity in self.entities:
            if entity.name == name and not entity.dead:
                self._entityNameCache[name] = entity
                return entity
        return None

    def getEntitiesOfLayer(self, layer: int) -> list[Entity]:
        if layer in self._entityLayerCache:
            return self._entityLayerCache[layer]
        else:
            self._entityLayerCache[layer] = []
        for entity in self.entities:
            if entity.layer == layer and not entity.dead:
                self._entityLayerCache[layer].append(entity)
                yield entity
                
    def _refreshLayerCache(self):
        self._entityLayerCache = {}
        for entity in (self.entities+self.inactiveEntities):
            if entity.dead: continue
            if entity.layer not in self._entityLayerCache:
                self._entityLayerCache[entity.layer] = []
            self._entityLayerCache[entity.layer].append(entity)
