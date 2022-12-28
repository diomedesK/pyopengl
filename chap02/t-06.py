from OpenGL.GL import *

from core.Base import Base
from core.Attribute import Attribute
from core.Uniform import Uniform
from core.OpenGLUtils import OpenGLUtils


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

        print("Attributing data...")
        Attribute("vec3", [ [0.0, 0.2, 0.0], [0.2, -0.2, 0.0], [-0.2, -0.2, 0.0] ]
                  ).associateVariable(self.program, "position")
        
        self.color1 = Uniform(self.program, "baseColor");
        self.color1.setData("vec3", [1.0, 1.0, 0.0])
        
        self.translation1 = Uniform(self.program, "translation");
        self.translation1.setData("vec3", [-0.5, 0.0, 0.0])

        self.color2 = Uniform(self.program, "baseColor");
        self.color2.setData("vec3", [1.0, 0.2, 0.3])
        
        self.translation2 = Uniform(self.program, "translation");
        self.translation2.setData("vec3", [0.5, 0.0, 0.0])


        # bcolor_ref = glGetUniformLocation(self.program, "translation")
        # glUniform3f(bcolor_ref, 0.5, 0.5, 0.1)

        

    def update(self):
        glUseProgram(self.program);

        self.translation1.uploadData()
        self.color1.uploadData()
        glDrawArrays(GL_LINE_LOOP, 0, 3)
        
        self.translation2.uploadData()
        self.color2.uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, 3)

        pass
    
    def main(self):
        pass

Executor(Base).run()
