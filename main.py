import os
os.add_dll_directory(os.getcwd()+"/libs/GLFW")
from common.settings import AppSettings
from geditor.editor import GatorEditor

def main():
    settings = AppSettings(
        "auto", "auto", "Gator Engine Editor [Test]", "main", "test")
    editor = GatorEditor(settings)
    editor.run()


if __name__ == "__main__":
    main()
