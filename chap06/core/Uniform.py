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

        if self.dataType == 'Light':
            self.variableRef = {
                "lightType":    glGetUniformLocation(program, variableName + ".lightType"),
                "color":        glGetUniformLocation(program, variableName + ".color"),
                "direction":    glGetUniformLocation(program, variableName + ".direction"),
                "position":     glGetUniformLocation(program, variableName + ".position"),
                "attenuation":  glGetUniformLocation(program, variableName + ".attenuation"),
            }
        else:
            self.variableRef = glGetUniformLocation(program, variableName)

        if self.variableRef == -1:
            print(f"WARNING\nThe uniform variable \"{variableName}\" does not exist in program {program}.")

    def setData(self, dataType, data):
        self.dataType = dataType
        self.data = data
    
    def uploadData(self):
        # print(f"Uploading {self.dataType} data for {self.variableName}")

        if self.variableRef == -1:
            print(self.variableName)
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
        elif self.dataType == "Light":
            direction = self.data.getDirection()
            position = self.data.getPosition()

            glUniform1i(self.variableRef["lightType"], self.data.lightType)
            glUniform3f(self.variableRef["color"], *self.data.color)
            glUniform3f(self.variableRef["direction"], *direction)
            glUniform3f(self.variableRef["position"], *position)
            glUniform3f(self.variableRef["attenuation"], *self.data.attenuation)

        else:
            print(f"Received unknown datatype for variable '{self.variableName}': {self.dataType} ")
