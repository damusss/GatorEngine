import glm


class Camera:
    def __init__(self):
        self.position: glm.vec3 = glm.vec3(0, 0, 0)
        self.zoom: float = 1.0
        self.proj: glm.mat4x4 = glm.ortho(-8, 8, -4, 4, -100, 100)
        self.view: glm.mat4x4 = glm.translate(glm.mat4(), self.position)

    def update(self):
        self.view = glm.translate(glm.scale(glm.mat4(1.0), glm.vec3(
            self.zoom, self.zoom, self.zoom)), self.position)
