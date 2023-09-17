import glm

class Colors:
    RED = glm.vec4(1,0,0,1)
    GREEN = glm.vec4(0,1,0,1)
    BLUE = glm.vec4(0,0,1,1)
    PURPLE = glm.vec4(1,0,1,1)
    YELLOW = glm.vec4(1,1,0,1)
    CYAN = glm.vec4(0,1,1,1)
    ORANGE = glm.vec4(1,0.5,0,1)
    WHITE = glm.vec4(1,1,1,1)
    BLACK = glm.vec4(0,0,0,1)
    LGRAY = glm.vec4(0.8,0.8,0.8,1)
    DGRAY = glm.vec4(0.2,0.2,0.2,1)
    GRAY = glm.vec4(0.5,0.5,0.5,1)
    INVISIBLE = glm.vec4(0,0,0,0)
     
    @staticmethod
    def dark(color:glm.vec4, factor:float = 0.5):
        return glm.vec4(color.x*factor, color.y*factor, color.z*factor, color.w*factor)