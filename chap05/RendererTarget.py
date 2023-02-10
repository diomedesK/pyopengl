import pygame
from OpenGL.GL import *

from core.Texture import Texture

class RenderTarget(object):
    def __init__(self, resolution = [512, 512], texture = None, properties = {} ):
        self.width, self.height = resolution

        if texture is not None:
            self.texture = texture
        else:
            self.texture = Texture(None, {
                "magFilter" : GL_LINEAR,
                "minFilter" : GL_LINEAR,
                "wrap" : GL_REPEAT
                })

            self.texture.setProperties(properties)
            self.texture.surface = pygame.Surface(resolution)
            self.texture.uploadData()

        # generate framebuffer and bind it
        # bind texture reference to generated framebuffer
        # generate depth buffer and attach it to generated framebuffer (using the glRenderbuffer* functions)

        # check framebuffer status; raise exception if the case

        framebufferRef = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, framebufferRef)

        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.texture.textureReference, 0)

        depthBufferRef = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depthBufferRef)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthBufferRef)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Framebuffer status error")
