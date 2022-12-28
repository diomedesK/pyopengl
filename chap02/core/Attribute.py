from OpenGL.GL import *;
import numpy

# This class associates glsl vertex shader program variables (that one starting with 'in' ) with 
# a buffer. I.E, it allows you to pass data from your buffer to the program

# that variable which receives data from a buffer is called "attribute variable", hence the name of this class


class Attribute(object):

    def __init__(self, dataType, data):
        
        #datatype ∈ [ int | float | vec2 | vec3 | vec4 ]
        
        self.buffer = glGenBuffers(1);
        self.dataType = dataType;
        self.data = data;

        self.uploadData();

    def uploadData(self):
        #numpy part just adapts data to required opengl standards i guess
        data = numpy.array(self.data).astype(numpy.float32) 
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

        # I wonder if isn't dangerous to let a buffer bound like this
        pass

    def associateVariable(self, program, variableName):
        
        target_variable = glGetAttribLocation(program, variableName)
        if target_variable == - 1:
            return

        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

        if self.dataType == "int":
            glVertexAttribPointer(target_variable, 1, GL_INT, False, 0, None )
        elif self.dataType == "float":
            glVertexAttribPointer(target_variable, 1, GL_FLOAT, False, 0, None )
        elif self.dataType == "vec2":
            glVertexAttribPointer(target_variable, 2, GL_FLOAT, False, 0, None )
        elif self.dataType == "vec3":
            glVertexAttribPointer(target_variable, 3, GL_FLOAT, False, 0, None )
        elif self.dataType == "vec4":
            glVertexAttribPointer(target_variable, 4, GL_FLOAT, False, 0, None )
        else:
            raise Exception(f"Invalid attribute. Unknown datatype ({self.dataType}) for variable '{variableName}'")

        #enables streaming of data from bound buffer to variable
        #'User-defined input values to vertex shaders are sometimes called "vertex attributes".'
        glEnableVertexAttribArray(target_variable)
