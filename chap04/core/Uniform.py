from OpenGL.GL import *

class Uniform(object):

    def __init__(self, program, variable_name):
        self.variable_name = variable_name
        self.variable_ref = glGetUniformLocation(program, variable_name)

        if self.variable_ref == -1:
            raise Exception(f"The uniform variable \"{variable_name}\" does not exist in the given program.")

    def setData(self, data_type, data):
        self.data_type = data_type
        self.data = data
    
    def uploadData(self):
        if self.variable_ref == -1:
            return 

        data = self.data
        # int | bool | float | vec2 | vec3 | vec4
        if self.data_type == "int":
            glUniform1i(self.variable_ref, data)
        elif self.data_type == "bool":
            glUniform1i(self.variable_ref, data)
        elif self.data_type == "float":
            glUniform1f(self.variable_ref, data)
        elif self.data_type == "vec2":
            glUniform2f(self.variable_ref, data[0], data[1])
        elif self.data_type == "vec3":
            glUniform3f(self.variable_ref, data[0], data[1], data[2])
        elif self.data_type == "vec4":
            glUniform4f(self.variable_ref, data[0], data[1], data[2], data[3])
        elif self.data_type == "mat4":
            glUniformMatrix4fv(self.variable_ref, 1, GL_TRUE, data)

