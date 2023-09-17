from OpenGL.GL import *
import glm
import numpy

import common.error as error


class Shader:
    def __init__(self, vertexSource: str, fragmentSource: str):
        self.ID: int = glCreateProgram()

        vertID = singleShaderBuilderHelper(GL_VERTEX_SHADER, vertexSource)
        fragID = singleShaderBuilderHelper(GL_FRAGMENT_SHADER, fragmentSource)

        glAttachShader(self.ID, vertID)
        glAttachShader(self.ID, fragID)

        glLinkProgram(self.ID)

        if not glGetProgramiv(self.ID, GL_LINK_STATUS):
            message = glGetProgramInfoLog(self.ID)
            error.fatal(error.ShaderError,
                        f"Could not link shader:\n{message}")

        glValidateProgram(self.ID)

        if not glGetProgramiv(self.ID, GL_VALIDATE_STATUS):
            message = glGetProgramInfoLog(self.ID)
            error.fatal(error.ShaderError,
                        f"Could not validate shader:\n{message}")

        glDeleteShader(vertID)
        glDeleteShader(fragID)

    def destroy(self):
        glDeleteProgram(self.ID)
        return self

    def use(self):
        glUseProgram(self.ID)
        return self

    def detach(self):
        glUseProgram(GL_NONE)
        return self

    def uniform1F(self, name: str, x: float):
        self.use()
        glUniform1f(self.getLocation(name), float(x))
        return self

    def uniform2F(self, name: str, x: float, y: float):
        self.use()
        glUniform2f(self.getLocation(name), float(x), float(y))
        return self

    def uniform3F(self, name: str, x: float, y: float, z: float):
        self.use()
        glUniform3f(self.getLocation(name), float(x), float(y), float(z))
        return self

    def uniform4F(self, name: str, x: float, y: float, z: float, w: float):
        self.use()
        glUniform4f(self.getLocation(name), float(x),
                    float(y), float(z), float(w))
        return self

    def uniform1I(self, name: str, x: int):
        self.use()
        glUniform1i(self.getLocation(name), int(x))
        return self

    def uniform2I(self, name: str, x: int, y: int):
        self.use()
        glUniform2i(self.getLocation(name), int(x), int(y))
        return self

    def uniform3I(self, name: str, x: int, y: int, z: int):
        self.use()
        glUniform3i(self.getLocation(name), int(x), int(y), int(z))
        return self

    def uniform4I(self, name: str, x: int, y: int, z: int, w: int):
        self.use()
        glUniform4i(self.getLocation(name), int(x), int(y), int(z), int(w))
        return self

    def uniformMat3F(self, name: str, mat: glm.mat3x3):
        self.use()
        glUniformMatrix3fv(self.getLocation(name), 1,
                           GL_FALSE, glm.value_ptr(mat))
        return self

    def uniformMat4F(self, name: str, mat: glm.mat4x4):
        self.use()
        glUniformMatrix4fv(self.getLocation(name), 1,
                           GL_FALSE, glm.value_ptr(mat))
        return self

    def uniformFloatArray(self, name: str, floatArray: list[float]):
        self.use()
        glUniform1fv(self.getLocation(name), 1,
                     numpy.array(floatArray, "float").tobytes())
        return self

    def uniformIntArray(self, name: str, intArray: list[int]):
        self.use()
        glUniform1iv(self.getLocation(name), 1,
                     numpy.array(intArray, "int").tobytes())
        return self

    def getLocation(self, name: str) -> int:
        loc = glGetUniformLocation(self.ID, name)
        if loc == -1:
            error.warning(
                error.ShaderError, f"Shader uniform '{name}' does not exist / is not used")
        return loc

    @classmethod
    def fromFile(self, fileName: str):
        with open(f"assets/shaders/{fileName}", "r") as shaderFile:
            vertSource = ""
            fragSource = ""
            mode = -1
            content = shaderFile.readlines()
            for line in content:
                if line.startswith("#shader") and "vertex" in line:
                    mode = 0
                elif line.startswith("#shader") and "fragment" in line:
                    mode = 1
                else:
                    if mode == 0:
                        vertSource += line+"\n"
                    elif mode == 1:
                        fragSource += line+"\n"
            return Shader(vertSource, fragSource)


def singleShaderBuilderHelper(type: int, source: str) -> int:
    ID = glCreateShader(type)
    glShaderSource(GLhandle(ID), [source])
    glCompileShader(ID)

    if not glGetShaderiv(ID, GL_COMPILE_STATUS):
        message = glGetShaderInfoLog(ID)
        error.fatal(error.ShaderError,
                    f"Could not compile {'vertex' if type == GL_VERTEX_SHADER else 'fragment'} shader:\n{message}")
    return ID
