from OpenGL.GL import *

from core.Base import Base
from core.Attribute import Attribute
from core.Uniform import Uniform
from core.OpenGLUtils import OpenGLUtils

import math

class Executor(Base):
    """docstring for Executor"""
    def __init__(self, arg):
        super(Executor, self).__init__()
        self.arg = arg

    def initialize(self):

        self.program = OpenGLUtils.initializeProgram(
                open("./glsl/t-06_v.glsl").read(),
                open("./glsl/t-06_f.glsl").read(),
                )

        glClearColor(0.0, 0.0, 0.0, 1.0);
        glPointSize(10);
        glLineWidth(5);

        print("Attributing data...")
        vdata = [ 
                 [0.0, 0.5, 0.0],
                 [0.0, -0.5, 0.0],
                 [-0.3, 0.1, 0.0],
                 [+0.3, 0.1, 0.0],

                 ]
        Attribute("vec3", vdata).associateVariable(self.program, "position")
        self.vlen = len(vdata)


        self.color = Uniform(self.program, "baseColor");
        self.color.setData("vec3", [1.0, 1.0, 0.0])
        
        self.translation = Uniform(self.program, "translation");
        self.translation.setData("vec3", [-0.5, 0.0, 0.0])

    def update(self):

        self.translation.data[0] = 0.75 *  math.sin(self.timer * 1.5)
        self.translation.data[1] = 0.75 *  math.cos(self.timer * 1.5)

        self.color.data[0] = 0.5 + 0.50 *  math.sin(self.timer)
        self.color.data[1] = 0.5 + 0.50 *  math.cos(self.timer)
        self.color.data[2] = 0.5 + 0.50 *  math.sin(self.timer)

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.program);

        self.translation.uploadData()
        self.color.uploadData()
        glDrawArrays(GL_LINES, 0, self.vlen)
        
        pass
    
    def main(self):
        pass

Executor(Base).main()

