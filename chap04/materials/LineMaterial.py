from OpenGL.GL import *

from materials.BasicMaterial import BasicMaterial

# sheer copypaste

class LineMaterial(BasicMaterial):
    def __init__(self, properties={}):
        super().__init__()

        #default values

        self.settings["drawStyle"] = GL_LINES
        self.settings["lineWidth"] = 1
        self.setProperties(properties)
    
    def updateRenderSettings(self):
        glLineWidth(self.settings["lineWidth"])
