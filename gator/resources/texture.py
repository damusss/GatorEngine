from OpenGL.GL import *
import PIL.Image as PillowImage


class Texture:
    def __init__(self, fileName: str):
        self.assetName = "UnregisteredTexture"
        self.fileName: str = fileName
        pillowImage = PillowImage.open(
            f"assets/images/{fileName}").transpose(PillowImage.FLIP_TOP_BOTTOM)
        imageData = pillowImage.tobytes()

        self.ID: int = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.ID)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        self.width, self.height = pillowImage.width, pillowImage.height
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.width,
                     self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)

        pillowImage.close()
        self.unbind()

    def destroy(self):
        glDeleteTextures(1, [self.ID])
        return self

    def bind(self, slot: int = 0):
        glActiveTexture(GL_TEXTURE0+slot)
        glBindTexture(GL_TEXTURE_2D, self.ID)
        return self

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, GL_NONE)
        return self
