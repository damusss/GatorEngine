import typing
if typing.TYPE_CHECKING:
    from ..gator.application import Application
    from ..geditor.editor import GatorEditor


class Singletons:
    editor: "GatorEditor" = None
    app: "Application" = None
