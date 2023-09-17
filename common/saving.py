import glm

from gator.resources.assets import Assets
from gator.resources.texture import Texture
from gator.resources.sprite import Sprite


def saveVec2(vec: glm.vec2) -> list[float]:
    return [vec.x, vec.y]


def saveVec3(vec: glm.vec3) -> list[float]:
    return [vec.x, vec.y, vec.z]


def saveVec4(vec: glm.vec4) -> list[float]:
    return [vec.x, vec.y, vec.z, vec.w]


def loadVec2(vec: list[float]) -> glm.vec2:
    return glm.vec2(vec[0], vec[1])


def loadVec3(vec: list[float]) -> glm.vec3:
    return glm.vec3(vec[0], vec[1], vec[2])


def loadVec4(vec: list[float]) -> glm.vec4:
    return glm.vec4(vec[0], vec[1], vec[2], vec[3])


def saveTexture(texture: Texture | None) -> str:
    if texture is None:
        return None
    return texture.assetName


def loadTexture(texture: str | None) -> Texture:
    if texture is None:
        return None
    return Assets.getTexture(texture)


def saveSprite(sprite: Sprite) -> dict:
    return {
        "texCoords": [
            saveVec2(coord) for coord in sprite.texCoords
        ],
        "texture": saveTexture(sprite.texture)
    }


def loadSprite(sprite: dict[str, list[list[float]] | str]) -> Sprite:
    return Sprite(
        loadTexture(sprite["texture"]),
        [loadVec2(coord) for coord in sprite["texCoords"]]
    )
