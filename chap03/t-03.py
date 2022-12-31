from OpenGL.GL import *

from core.Base import Base
from core.OpenGLUtils import OpenGLUtils
from core.Attribute import Attribute
from core.Matrix import Matrix

from core.Uniform import Uniform

class Executor(Base):

    def initialize(self):
        self.program = OpenGLUtils.initializeProgram(
                open("./glsl/t-03_v.glsl").read(),
                open("./glsl/t-03_f.glsl").read()
                )

        self.VAO_tri = glGenVertexArrays(1)
        glBindVertexArray(self.VAO_tri)

        glPointSize(10)
        
        triangle_vertices = [
            [0.0, 0.2, 0.0],
            [0.1, -0.2, 0.0],
            [-0.1, -0.2, 0.0]
        ]

        self.tri_len = len(triangle_vertices)
        Attribute("vec3", triangle_vertices).associateVariable(self.program, "position")

        self.model_matrix = Uniform(self.program, "modelMatrix")
        self.projection_matrix = Uniform(self.program, "projectionMatrix")

        self.model_matrix.setData("mat4", Matrix.makeTranslation(0, 0, -1))
        self.projection_matrix.setData("mat4", Matrix.makePerspective())

        self.MOVE = 10 / self.frameRate
        self.MOVE = 0.05 * self.MOVE 
        
        self.turnSpeed = 90 * ( 3.14/180 )
    
    def update(self):
        turnAmount = self.turnSpeed * self.deltaTime

        if len(self.input.keyPressedList) > 0:
            print(self.input.keyPressedList)

        # The result of all transformations is stored in the matrix "model_matrix"
        # The current position is calculated as the product of the original vertices 
        # (stored in the "position" attribute in the vertex shader) with the model matrix.
        print(self.model_matrix.data)

        # Think of global transformations as the movement in relation to something
        # e.g. the cardinal points, and the local transformations in relation to itself.

        # GLOBAL TRANSLATIONS
        # T * M 
        if self.input.isKeyPressed("w"):
            m = Matrix.makeTranslation(0, self.MOVE, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.isKeyPressed("s"):
            m = Matrix.makeTranslation(0, -self.MOVE, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.isKeyPressed("a"):
            m = Matrix.makeTranslation(-self.MOVE, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.isKeyPressed("d"):
            m = Matrix.makeTranslation(self.MOVE, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.isKeyPressed("z"):
            m = Matrix.makeTranslation(0, 0, self.MOVE)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.isKeyPressed("x"):
            m = Matrix.makeTranslation(0, 0, -self.MOVE)
            self.model_matrix.data = m @ self.model_matrix.data 

        # LOCAL TRANSLATIONS (it's the same as global, but the order of the 
        # matrix multiplication is inverted)
        # M * T * M' M  == M * T (The product of M time it's identity always equals one)

        if self.input.isKeyPressed("i"):
            m = Matrix.makeTranslation(0, self.MOVE, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.isKeyPressed("k"):
            m = Matrix.makeTranslation(0, -self.MOVE, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.isKeyPressed("j"):
            m = Matrix.makeTranslation(-self.MOVE, 0, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.isKeyPressed("l"):
            m = Matrix.makeTranslation(self.MOVE, 0, 0)
            self.model_matrix.data = self.model_matrix.data @ m

        if self.input.isKeyPressed("n"):
            m = Matrix.makeTranslation(0, 0, self.MOVE)
            self.model_matrix.data = self.model_matrix.data @ m

        if self.input.isKeyPressed("m"):
            m = Matrix.makeTranslation(0, 0, -self.MOVE)
            self.model_matrix.data = self.model_matrix.data @ m


        # GLOBAL ROTATION (around the world-origin)
        if self.input.isKeyPressed("q"):
            m = Matrix.makeRotationZ(turnAmount)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.isKeyPressed("e"):
            m = Matrix.makeRotationZ(-turnAmount)
            self.model_matrix.data = m @ self.model_matrix.data

        # LOCAL ROTATION (around the center of the shape)
        if self.input.isKeyPressed("u"):
            m = Matrix.makeRotationZ(turnAmount)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.isKeyPressed("o"):
            m = Matrix.makeRotationZ(-turnAmount)
            self.model_matrix.data = self.model_matrix.data @ m


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # pyright: ignore
        glUseProgram(self.program)

        glBindVertexArray(self.VAO_tri)

        self.projection_matrix.uploadData()
        self.model_matrix.uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.tri_len)
        

    def main(self):
        vertexShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        out vec3 color;

        void main() {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            color = vertexColor;
        }
        """
        fragmentShaderCode = """
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        in vec3 color;
        out vec4 fragColor;

        void main() {
            vec4 tempColor = vec4(baseColor, 1.0);
            if ( useVertexColors ) tempColor *= vec4(color, 1.0);
            fragColor = tempColor;
        }
        """

        OpenGLUtils.initializeProgram(vertexShaderCode, fragmentShaderCode)


# Executor().run()
Executor().main()

