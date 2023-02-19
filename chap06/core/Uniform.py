from OpenGL.GL import *
from typing import Union
from light.Light import Light
import logging

from numpy import ndarray

logger = logging.getLogger(__name__)

class Uniform(object):

    def __init__(self, program, variableName):
        if ( program is None ) or ( variableName is None ):
            return 

        self.dataType: Union[str, None] = None
        self.data: Union[int, dict, list] = 0

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
            return 

        def sampler2DHandler(data: list):
            textureObjectReference, textureUnitReference = data
            glActiveTexture(GL_TEXTURE0 + textureUnitReference)
            glBindTexture(GL_TEXTURE_2D, textureObjectReference)
            glUniform1i(self.variableRef, textureUnitReference)

        def lightHandler(data: Light):
            direction = data.getDirection()
            position = data.getPosition()

            glUniform1i(self.variableRef["lightType"], data.lightType)
            glUniform3f(self.variableRef["color"], *data.color)
            glUniform3f(self.variableRef["direction"], *direction)
            glUniform3f(self.variableRef["position"], *position)
            glUniform3f(self.variableRef["attenuation"], *data.attenuation)

        acceptedDataTypes = {
                int: [ "float" ],
                bool: [ "bool"],
                float: [ "float" ],
                list: [ "vec2", "vec3", "vec4", "sampler2D" ],
                ndarray: [ "mat4" ],
                Light: [ "Light" ]
                }

        # 'Invert' the object, so the value is now used to access the key 
        acceptedDataTypes = { el: key for key, value in acceptedDataTypes.items() for el in value }

        dataHandlesIndexer = {
            'int':	        [ glUniform1i, False ],
            'bool':	        [ glUniform1i, False ],
            'float':	    [ glUniform1f, False ],
            'vec2':	        [ glUniform2f, False ],
            'vec3':	        [ glUniform3f, False ],
            'vec4':	        [ glUniform4f, False ],
            'mat4':	        [ lambda data: glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, data), True],
            'sampler2D':    [ sampler2DHandler, True ],
            'Light':	    [ lightHandler, True ]
        }

        if self.dataType in dataHandlesIndexer:
            dataHandler, isWrapper = dataHandlesIndexer[self.dataType]
            if not isinstance( self.data, acceptedDataTypes[self.dataType] ):
                raise Exception(f"{type(self.data)} is not allowed for '{self.dataType}'")
            else:
                try:
                    if isWrapper:
                        dataHandler(self.data) 
                    elif isinstance(self.data, list):
                        dataHandler(self.variableRef, *self.data)
                    else:
                        dataHandler(self.variableRef, self.data)

                except Exception as err:
                    logger.exception(f"Error processing data-type {self.dataType}: {err}")
                    raise 

        else:
            logger.warning(f"ALERT: Received unknown datatype for variable 'self.variableName': {self.dataType} ")
