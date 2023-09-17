import os
os.add_dll_directory(os.getcwd()+"/libs/GLFW")
from gator.common.settings import AppSettings
from geditor.editor import GatorEditor

def main():
    settings = AppSettings(
        "auto", "auto", True, "Gator Engine Editor [Test]", "main", "test", "projects.", None, None)
    editor = GatorEditor(settings)
    editor.run()


if __name__ == "__main__":
    main()
