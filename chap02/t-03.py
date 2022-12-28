from core.Base  import Base
from core.Attribute import Attribute

from OpenGL.GL import *
from core.OpenGLUtils import OpenGLUtils 

VERTEX_COUNT = 'vertex_count'
VAO = 'vao'
POS = 'pos'
TRIANGLE = 'triangle'
SQUARE = 'square'

class Executor(Base):

    def __init__(self):
        super().__init__()
        self.shapes = {
                'triangle': {},
                'square': {}
                }

    def initialize(self):

        vertexShaderCode = """
            in vec3 position;
            void main()
            {
              gl_Position = vec4(position.x, position.y, position.z, 1.0);
            }
        """

        self.program = OpenGLUtils.initializeProgram( 
                                                     open("./glsl/t-03_v.glsl").read(),
                                                     open("./glsl/t-02_f.glsl").read()
                                                     )

        triangleVAO = glGenVertexArrays(1)
        glBindVertexArray(triangleVAO)
        self.shapes[TRIANGLE][VAO] = triangleVAO
        self.shapes[TRIANGLE][POS] = [
                [-0.5, 0.8, 0.0], 
                [-0.2, 0.2, 0.0],
                [-0.8, 0.2, 0.0]
                ]
        self.shapes[TRIANGLE][VERTEX_COUNT] = len(self.shapes[TRIANGLE][POS])
        Attribute("vec3", self.shapes[TRIANGLE][POS]).associateVariable(self.program, "position")

        squareVAO = glGenVertexArrays(1)
        glBindVertexArray(squareVAO)
        self.shapes[SQUARE][VAO] = squareVAO
        self.shapes[SQUARE][POS] = [
                [0.8, 0.8, 0.0],
                [0.8, 0.2, 0.0],
                [0.2, 0.2, 0.0],
                [0.2, 0.8, 0.0]
                ]
        self.shapes[SQUARE][VERTEX_COUNT] = len(self.shapes[SQUARE][POS])
        Attribute("vec3", self.shapes[SQUARE][POS]).associateVariable(self.program, "position")

        pass

    def update(self):
        glUseProgram(self.program)
        glBindVertexArray(self.shapes[TRIANGLE][VAO])
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.shapes[TRIANGLE][VERTEX_COUNT])

        glBindVertexArray(self.shapes[SQUARE][VAO])
        glDrawArrays(GL_LINE_LOOP, 0, self.shapes[SQUARE][VERTEX_COUNT])


Executor().run()
