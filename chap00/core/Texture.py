import pygame
from OpenGL.GL import *

class Texture(object):
    """Texture object generator"""
    def __init__(self, imagePath=None, properties={}):
        super().__init__()

        self.surface = None
        self.textureReference = glGenTextures(1)

        self.properties = {
                "magFilter": GL_LINEAR,
                "minFilter": GL_LINEAR_MIPMAP_LINEAR,
                "wrap": GL_REPEAT
                }

        self.setProperties(properties)

        if imagePath is not None:
            self.loadImage(imagePath)
            self.uploadData()

    
    def loadImage(self, path):
        self.surface = pygame.image.load(path)
    
    def setProperties(self, properties):
        availableProperties = self.properties.keys()
        for key, value in properties.items():
            if key in availableProperties:
                self.properties[key] = value
            else:
                raise Exception("Texture has no property \"{}\"".format(key))

    def uploadData(self):
        if self.surface is None:
            return
        
        # you have to flip it because for some reason it comes inverted by default (like why?)
        data = pygame.image.tostring(self.surface, "RGBA", True)

        width = self.surface.get_width()
        height = self.surface.get_height()
        glBindTexture(GL_TEXTURE_2D, self.textureReference)

        #glTexImage2D( bindTarget, level, internalFormat, width, height, border, format, type, pixelData )
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data )
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.properties["magFilter"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.properties["minFilter"])
        
        # the texture_wrap (s, t) specifies how to handle uv components (also usually named (s,t) )
        # that run outside the [0, 1] range
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.properties["wrap"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.properties["wrap"])

        # set border as white
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [0,0.5,0.5,1])

