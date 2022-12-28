from core.Base import Base
from core.Attribute import Attribute
from core.OpenGLUtils import OpenGLUtils

from OpenGL.GL import *
import numpy

class Executor(Base):
    
    def __init__(self):
        super().__init__()

    def initialize(self):

        self.program = OpenGLUtils.initializeProgram(
                open("./glsl/t-05_v.glsl").read(),
                open("./glsl/t-05_f.glsl").read()
                )

        position_d = [
                [0.8, 0.0, 0.0],
                [0.4, 0.6, 0.0],
                [-0.4, 0.6, 0.0],
                [-0.8, 0.0, 0.0],
                [-0.4, -0.6, 0.0],
                [0.4, -0.6, 0.0]
                ]

        #both  must have the same length
        color_d = [
                [1.0, 0.0, 0.0],
                [1.0, 0.5, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.5, 0.0, 1.0] 
                ]

        Attribute("vec3", position_d).associateVariable(self.program, "position")
        # Attribute("vec3", color_d).associateVariable(self.program, "vertex_color")
        # doing the line above manually be like:
        cb = glGenBuffers(1);

        glBindBuffer(GL_ARRAY_BUFFER, cb)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(color_d).astype(numpy.float32).ravel(), GL_STATIC_DRAW)

        ca = glGetAttribLocation(self.program, "vertex_color")
        glBindBuffer(GL_ARRAY_BUFFER, cb)
        glVertexAttribPointer(ca, 3, GL_FLOAT, False, 0, None )
        glEnableVertexAttribArray(ca)

        #optional (you aint gonna see no point if you dont do this)
        glPointSize(10);
        glLineWidth(4)

        self.v_len = len(position_d)

        pass
    
    def update(self):
        glUseProgram(self.program);

        # glDrawArrays(GL_POINTS, 0, self.v_len )
        # glDrawArrays(GL_LINES, 0, self.v_len )
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.v_len)

        pass

Executor().run()
