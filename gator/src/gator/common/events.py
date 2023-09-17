def auto_event_type() -> int:
    auto_event_type.count += 1
    return auto_event_type.count


auto_event_type.count = -1

USEREVENT: int = auto_event_type()
COMP_ADDED: int = auto_event_type()
COMP_REMOVED: int = auto_event_type()
SCENE_SAVED: int = auto_event_type()
SCENE_LOADED: int = auto_event_type()


class Event:
    def __init__(self, type: int, userEventType: int = -1, **attrs):
        self.type: int = type
        self.userEventType: int = userEventType
        for name, val in attrs.items():
            setattr(self, name, val)


class EventSystem:
    observers: dict[int, list] = {num: []
                                  for num in range(auto_event_type.count)}
    observersAllEvents: list = []

    @classmethod
    def register(cls, eventTypes: list[int] | tuple[int], callbackFunc):
        if isinstance(eventTypes, list | tuple):
            for eType in eventTypes:
                if not eType in cls.observers:
                    cls.observers[eType] = []
                cls.observers[eType].append(callbackFunc)
        else:
            if not eventTypes in cls.observers:
                cls.observers[eventTypes] = []
            cls.observers[eventTypes].append(callbackFunc)

    @classmethod
    def registerAll(cls, callbackFunc):
        cls.observersAllEvents.append(callbackFunc)

    @classmethod
    def invoke(cls, eventType: int, userEventType: int = -1, **attrs) -> Event:
        if not eventType in cls.observers:
            cls.observers[eventType] = []
        event = Event(type, userEventType, **attrs)
        for callbackFunc in cls.observersAllEvents:
            callbackFunc(event)
        for callbackFunc in cls.observers[eventType]:
            callbackFunc(event)
        return event


def invoke(eventType: int, userEventType: int = -1, **attrs) -> Event:
    return EventSystem.invoke(eventType, userEventType, **attrs)


def register(eventTypes: tuple[int] | list[int], func):
    EventSystem.register(eventTypes, func)


def registerAll(func):
    EventSystem.registerAll(func)
