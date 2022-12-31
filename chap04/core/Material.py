from core.OpenGLUtils import OpenGLUtils
from core.Uniform import Uniform

# This is a base class which stores the program references (by compiling the 
# source code), the rendering settings and also the uniform variable values.

class Material(object):
    """Stores program references, uniforms and rendering settings"""
    def __init__(self, vertexShaderCode, fragmentShaderCode):
        super(Material, self).__init__()

        self.program = OpenGLUtils.initializeProgram(vertexShaderCode, fragmentShaderCode)

        self.uniforms = {}
        self.settings = {}

    def addUniform(self, variableName, dataType, data):
        # stores an uniform into the self.uniform dictionary
        self.uniforms[variableName] = Uniform.fromData(dataType, data)

        pass

    def locateUniforms(self):
        # locates uniforms stored in the self.uniform dictionary to the self.program

        for variableName, uniformObject in self.uniforms.items():
            uniformObject.locateVariable(self.program, variableName)

    def updateRenderSettings(self):
        pass

    # convenience method for setting multiple material "properties"
    # (uniform and render setting values) from a dictionary
    def setProperties(self, properties):
        for name, data in properties.items():
            if name in self.uniforms.keys():
                self.uniforms[name] = data
            elif name in self.settings.keys():
                self.settings[name] = data

            else:
                raise Exception(f"No property in Material named \"{name}\"")
