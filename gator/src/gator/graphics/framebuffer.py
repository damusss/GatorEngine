from OpenGL.GL import *
from gator.resources.texture import Texture
import gator.common.error as error


class Framebuffer:
    def __init__(self, width, height):
        self.width, self.height = width, height
        
        self.fboID = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fboID)
        
        self.texture:Texture = Texture.asFrameBuffer(width, height)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture.ID, 0)
        
        self.rboID = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rboID)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT32, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.rboID)
        #if (not glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
        #    error.fatal(error.OpenGLError, "Could not create/complete framebuffer")
        glBindFramebuffer(GL_FRAMEBUFFER, GL_NONE)
        
    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fboID)
    

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    