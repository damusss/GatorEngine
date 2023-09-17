import json
import importlib

from gator.core.camera import Camera
from gator.graphics.renderer import Renderer
from gator.entity import Entity

from gator.components.transform import Transform
from gator.components.component import Component
from gator.components.all import defaultComponents

import common.events as events
import common.saving as saving
from common.colors import Colors
from common.singletons import Singletons


class Scene:
    def __init__(self, name: str):
        self.name: str = name
        self.camera: Camera = Camera()
        self.renderer: Renderer = Renderer()
        self.entities: list[Entity] = []
        self.inactiveEntities: list[Entity] = []
        self.started: bool = False
        self.clearColor = Colors.BLACK
        self.allComponents: list[type[Component]] = defaultComponents

    def load(self):
        with open(f"geditor/projects/{Singletons.app.projectName}/{self.name}.ge", "r") as saveFile:
            data = json.load(saveFile)
            self.camera.position = saving.loadVec3(data["camera"]["pos"])
            self.camera.zoom = data["camera"]["zoom"]
            self.clearColor = saving.loadVec4(data["clearColor"])
            self.allComponents = importlib.import_module(
                f".projects.{Singletons.app.projectName}.allComponents", "geditor").allComponents
            for eData in data["entities"]:
                entity = Entity.fromFile(eData, self.allComponents)
                self.entities.append(entity)
            for eData in data["inactiveEntities"]:
                entity = Entity.fromFile(eData, self.allComponents)
                self.entities.append(entity)
                entity.active = False
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

    def save(self):
        saveData = {
            "entities": [entity.toFile() for entity in self.entities],
            "inactiveEntities": [entity.toFile() for entity in self.inactiveEntities],
            "camera": {
                "pos": saving.saveVec3(self.camera.position),
                "zoom": self.camera.zoom
            },
            "clearColor": saving.saveVec4(self.clearColor)
        }
        with open(f"geditor/projects/{Singletons.app.projectName}/{self.name}.ge", "w") as saveFile:
            json.dump(saveData, saveFile)

    def start(self):
        self.started = True
        for entity in self.entities:
            entity.start()

    def update(self):
        entitiesToRemove: list[Entity] = []
        for i in range(len(self.entities)-1):
            if self.entities[i].dead:
                entitiesToRemove.append(entity)
                continue
            self.entities[i].update()
        for entity in entitiesToRemove:
            entity.onDestroy()
            for comp in entity.components:
                events.invoke(events.COMP_REMOVED, component=comp)
            self.entities.remove(entity)
        self.camera.update()

    def editorUpdate(self):
        for entity in self.entities:
            entity.editorUpdate()

    def render(self, shader):
        self.renderer.render(shader)

    def destroy(self):
        self.renderer.destroy()
        for entity in self.entities:
            entity.onDestroy()

    def instantiate(self, name: str, layer: int) -> Entity:
        entity = Entity(name, layer)
        t = entity.addComponent(Transform())
        entity.transform = t
        if self.started:
            entity.start()
        self.entities.append(entity)
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
        return newEntity

    def getEntityByID(self, ID: int) -> Entity | None:
        for entity in self.entities:
            if entity.ID == ID:
                return entity
        return None

    def getEntityByName(self, name: str) -> Entity | None:
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None

    def getEntitiesOfLayer(self, layer: int) -> list[Entity]:
        for entity in self.entities:
            if entity.layer == layer:
                yield entity
