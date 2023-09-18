import typing
import imgui
import glm

if typing.TYPE_CHECKING:
    from ..entity import Entity
    
import gator.common.gimgui as gimgui


class Component:
    GLOBAL_ID: int = 0
    hideInProperties: list[str] = []

    def __init__(self, id: int = None, active: bool = True):
        self.ID: int = Component.GLOBAL_ID if not id else id
        if not id:
            Component.GLOBAL_ID += 1
        self.dead: bool = False
        self.active: bool = active
        self.entity: "Entity" = None

    @classmethod
    def fromFile(cls, cData: dict):
        return cls(cData["id"], cData["active"])

    def toFile(self):
        return {
            "id": self.ID,
            "active": self.active,
            "type": self.__class__.__name__
        }

    def start(self):
        ...

    def update(self):
        ...

    def editorUpdate(self):
        ...

    def baseImgui(self):
        if not "UID" in self.hideInProperties:
            imgui.text(f"UID: {self.ID}")
        if not "active" in self.hideInProperties:
            _, self.active = gimgui.checkbox("Active", self.active)
        for name, value in list(vars(self).items()):
            if not name.startswith("__") and \
                    not name.endswith("__") and \
                    not name in self.hideInProperties and \
                    not name in ["ID", "active", "dead", "entity", "GLOBAL_ID", "hideInProperties"] and \
                    not name.startswith("_") and \
                    not name.lower().startswith("ic"):

                originalName = name
                for prefix in ["ge_", "GE_", "ge", "GE"]:
                    if name.startswith(prefix):
                        name = name.replace(prefix, "", 1)
                        break
                if "_" in name:
                    name = name.replace("_", " ").title()
                else:
                    name = name[0].upper()+name[1::]

                match value:
                    case bool():
                        _, value = gimgui.checkbox(name, value)
                    case int():
                        _, value = gimgui.dragInt(name, value)
                    case float():
                        _, value = gimgui.dragFloat(name, value)
                    case str():
                        _, value = gimgui.inputText(name, value)
                    case glm.vec2():
                        _, value = gimgui.dragVec2(name, value)
                    case glm.vec3():
                        _, value = gimgui.dragVec3(name, value)
                    case glm.vec4():
                        _, value = gimgui.dragVec4(name, value)
                    case list() | tuple():
                        value = gimgui.iterable(name, value)
                setattr(self, originalName, value)

    def imgui(self):
        self.baseImgui()

    def onDestroy(self):
        ...

    def kill(self):
        self.dead = True

    def setActive(self, active: bool):
        self.active = active
