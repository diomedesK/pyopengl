from core.OpenGLUtils import OpenGLUtils
from core.Uniform import Uniform

from OpenGL.GL import *

class Material(object):
    """Stores program references, uniforms and rendering settings"""

    def __init__(self, vertexShaderCode, fragmentShaderCode):
        super(Material, self).__init__()
        self.program = OpenGLUtils.initializeProgram(vertexShaderCode, fragmentShaderCode)
        self.uniforms = {}
        self.settings = {}

        self.uniforms["modelMatrix"] = Uniform.fromData("mat4", None)
        self.uniforms["viewMatrix"] = Uniform.fromData("mat4", None)
        self.uniforms["projectionMatrix"] = Uniform.fromData("mat4", None)

        self.settings["drawStyle"] = GL_TRIANGLES

    def addUniform(self, dataType, name, data):
        self.uniforms[name] = Uniform.fromData(dataType, data)

    def locateUniforms(self):
        for uniformName, uniformObject in self.uniforms.items():
            uniformObject.locateUniform(self.program, uniformName)

    def updateRenderSettings(self):
        pass

    # quick way to initialize things
    def setProperties(self, properties):
        
        for propertyName, propertyValue in properties.items():
            if propertyName in self.uniforms.keys():
                self.uniforms[propertyName].data =  propertyValue
            elif propertyName in self.settings.keys():
                self.settings[propertyName].data =  propertyValue
            else:
                raise Exception(f"No property named {propertyName} in material ({id(self)})")

    
