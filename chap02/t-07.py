from OpenGL.GL import *

from core.Base import Base
from core.Attribute import Attribute
from core.Uniform import Uniform
from core.OpenGLUtils import OpenGLUtils

X_MOVE = 0.02

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

        print("Attributing data...")
        Attribute("vec3", [ [0.0, 0.2, 0.0], [0.2, -0.2, 0.0], [-0.2, -0.2, 0.0] ]
                  ).associateVariable(self.program, "position")

        
        self.color = Uniform(self.program, "baseColor");
        self.color.setData("vec3", [1.0, 1.0, 0.0])
        
        self.translation = Uniform(self.program, "translation");
        self.translation.setData("vec3", [-0.5, 0.0, 0.0])

        self.increment = X_MOVE

    def update(self):

        x_ = self.translation.data[0]
        if x_ < -1:
             self.increment = X_MOVE
        elif x_ > 1: 
            self.increment = -X_MOVE
        self.translation.data[0] += self.increment

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.program);

        self.translation.uploadData()
        self.color.uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, 3)
        

        
        pass
    
    def main(self):
        pass

Executor(Base).run()

