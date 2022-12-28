import sys
from OpenGL.GL import *

from core.OpenGLUtils import OpenGLUtils 
from core.Base import Base

class Executor(Base):

    def initialize(self):
        self.program = OpenGLUtils.initializeProgram(
                open("./glsl/t-02_v.glsl", "r").read(), 
                open("./glsl/t-02_f.glsl", "r").read()
                )

Executor().run()
