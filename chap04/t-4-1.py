import pygame
from OpenGL.GL import *

from core.OpenGLUtils import OpenGLUtils
from core.Attribute import Attribute
from core.Uniform import Uniform
from core.Matrix import Matrix

import numpy


class BoxGeometry():

    def __init__(self, width=1, height=1, depth=1):
        super().__init__()
        p0 = [-width*0.5, -height*0.5, -depth*0.5]
        p1 = [width*0.5, -height*0.5, -depth*0.5]
        p2 = [-width*0.5, height*0.5, -depth*0.5]
        p3 = [width*0.5, height*0.5, -depth*0.5]
        p4 = [-width*0.5, -height*0.5, depth*0.5]
        p5 = [width*0.5, -height*0.5, depth*0.5]
        p6 = [-width*0.5, height*0.5, depth*0.5]
        p7 = [width*0.5, height*0.5, depth*0.5]
        #colors for faces in order: x+, x-, y+, y-, z+, z-
        c1, c2 = [1, 0.5, 0.5], [0.5, 0, 0]
        c3, c4 = [0.5, 1, 0.5], [0, 0.5, 0]
        c5, c6 = [0.5, 0.5, 1], [0, 0, 0.5]

        self.positionData = [
            p5, p1, p3, p5, p3, p7,
            p0, p4, p6, p0, p6, p2,
            p6, p7, p3, p6, p3, p2,
            p0, p1, p5, p0, p5, p4,
            p4, p5, p7, p4, p7, p6, 
            p1, p0, p2, p1, p2, p3
        ]

        self.colorData = ([c1] + [c2] + [c3] + [c4] + [c5] + [c6])*6

        self.vertexCount = len(self.positionData)


class Graphics(object):
    """docstring for Executor"""
    def __init__(self, screenResolution=[512, 512]):
        pygame.init()
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL
        self.screen = pygame.display.set_mode( screenResolution, displayFlags )
        pygame.display.set_caption("System32")

        self.frameRate = 60
        self.clock = pygame.time.Clock()
        self.running = True

        self.deltaTime = 1000 / self.frameRate / 100
        self.time = 0

    def initialize(self):

        glPointSize(10)
        glLineWidth(5)
        glEnable(GL_CULL_FACE)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        self.boxGeometry = BoxGeometry()

        self.program = OpenGLUtils.initializeProgram(
                open("./glsl/vertexShader.glsl").read(),
                open("./glsl/fragmentShader.glsl").read(),
                )

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Vertex shader related

        self.worldMatrix = Matrix.makeTranslation(0, 0, 0)

        glUseProgram(self.program)
        
        self.projectionMatrix = Uniform.quickUpload(
                self.program, 
                "projectionMatrix", 
                "mat4", 
                Matrix.makePerspective()
                )

        self.modelMatrix = Uniform.quickUpload(
                self.program,
                "modelMatrix",
                "mat4",
                Matrix.makeTranslation(0, 0, 0)
                )

        self.viewMatrix = Uniform.quickUpload(
                self.program,
                "viewMatrix",
                "mat4",
                numpy.linalg.inv(self.worldMatrix) @ Matrix.makeTranslation(0, 0, -4)
                )

        Attribute("vec3", self.boxGeometry.positionData).associateVariable(self.program, "vertexPosition")
        Attribute("vec3", self.boxGeometry.colorData).associateVariable(self.program, "vertexColor")
        
        # Fragment shader related
        glUseProgram(self.program)
        Uniform.quickUpload(self.program, "baseColor", "vec3", [1.0, 1.0, 1.0])
        Uniform.quickUpload(self.program, "useVertexColors", "bool", True)
        glUseProgram(0)



    def update(self):
        pass

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pass
    
    def run(self):
        self.initialize()

        while(self.running):
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.program)
            self.handleInput()


            rotation = self.deltaTime * 0.05
            m = Matrix.makeRotationX(rotation) @ Matrix.makeRotationY(rotation * 0.9) @ Matrix.makeRotationZ(rotation * 0.8)
            self.modelMatrix.data = self.modelMatrix.data @ m
            self.modelMatrix.uploadData()

            glDrawArrays(GL_TRIANGLES, 0, self.boxGeometry.vertexCount)

            pygame.display.flip()
            self.clock.tick(self.frameRate)
            self.time += self.deltaTime

        pass
        
Graphics().run()
