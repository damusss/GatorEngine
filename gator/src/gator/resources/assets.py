from gator.graphics.shader import Shader
from gator.resources.texture import Texture

import gator.common.error as error


class Assets:
    shaders: dict[str, Shader] = {}
    textures: dict[str, Texture] = {}

    @classmethod
    def registerShader(cls, assetName: str, shader: Shader):
        cls.shaders[assetName] = shader
        return cls

    @classmethod
    def getShader(cls, assetName: str) -> Shader:
        if assetName not in cls.shaders:
            error.fatal(error.AssetError,
                        f"Shader '{assetName}' was not registered")
        return cls.shaders[assetName]

    @classmethod
    def registerTexture(cls, assetName: str, texture: Texture):
        cls.textures[assetName] = texture
        texture.assetName = assetName
        return cls

    @classmethod
    def getTexture(cls, assetName: str) -> Texture:
        if assetName not in cls.textures:
            error.warning(error.AssetError,
                        f"Texture '{assetName}' was not registered")
            return None
        return cls.textures[assetName]

    @classmethod
    def destroy(cls):
        for shader in cls.shaders.values():
            shader.destroy()
        for texture in cls.textures.values():
            texture.destroy()

    @classmethod
    def preRegister(cls):
        cls .registerShader("singleSprite", Shader.fromFile("assets/shaders/singleSprite.glsl"))\
            .registerShader("quad", Shader.fromFile("assets/shaders/quad.glsl"))\
            .registerShader("sprite", Shader.fromFile("assets/shaders/sprite.glsl"))\
            .registerTexture("pygame", Texture("assets/images/test/pygame.png"))\
            .registerTexture("peporito", Texture("assets/images/test/peporito.png"))
