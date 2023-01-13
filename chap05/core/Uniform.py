from OpenGL.GL import *

class Uniform(object):

    def __init__(self, program, variableName):
        if ( program is None ) or ( variableName is None ):
            return 

        self.dataType = 0
        self.data = 0

        self.locateUniform(program, variableName)
    
    @classmethod
    def fromData(cls, dataType, data):
        uniform =  cls(None, None)
        uniform.setData(dataType, data)
        return uniform


    @classmethod
    def quickUpload(cls, program, variableName, dataType, data):
        uniform = cls(program, variableName)
        uniform.setData(dataType, data)
        uniform.uploadData()
        return uniform

    def locateUniform(self, program, variableName):
        self.variableName = variableName
        self.variableRef = glGetUniformLocation(program, variableName)

        if self.variableRef == -1:
            raise Exception(f"The uniform variable \"{variableName}\" does not exist in the given program.")

    def setData(self, dataType, data):
        self.dataType = dataType
        self.data = data
    
    def uploadData(self):
        if self.variableRef == -1:
            return 

        data = self.data
        # int | bool | float | vec2 | vec3 | vec4
        if self.dataType == "int":
            glUniform1i(self.variableRef, data)
        elif self.dataType == "bool":
            glUniform1i(self.variableRef, data)
        elif self.dataType == "float":
            glUniform1f(self.variableRef, data)
        elif self.dataType == "vec2":
            glUniform2f(self.variableRef, data[0], data[1])
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef, data[0], data[1], data[2])
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef, data[0], data[1], data[2], data[3])
        elif self.dataType == "mat4":
            glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, data)
        elif self.dataType == "sampler2D":
            textureObjectReference, textureUnitReference = self.data
            glActiveTexture(GL_TEXTURE0 + textureUnitReference)
            glBindTexture(GL_TEXTURE_2D, textureObjectReference)
            glUniform1i(self.variableRef, textureUnitReference)
