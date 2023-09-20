from gator.resources.texture import Texture
from gator.graphics.shader import Shader
from gator.resources.assets import Assets
from gator.graphics.customrenderer import CustomRenderer
from gator.core.time import Time

PROJECT_PATH = "projects/GatorEngine_test/"
ASSETS_PATH = PROJECT_PATH+"assets/"
IMAGES_PATH = ASSETS_PATH+"images/"
SHADERS_PATH = ASSETS_PATH+"shaders/"

def testCustomShaderUniformLoader(shader: Shader):
    shader.uniform1F("uTime", Time.getTime())

def loadResources():
    Assets.registerTexture("purplebg", Texture(IMAGES_PATH+"purplebg.png"))
    Assets.registerShader("testCustom", Shader.fromFile(SHADERS_PATH+"testCustom.glsl"))
    CustomRenderer.registerUniformLoader("testCustom", testCustomShaderUniformLoader)