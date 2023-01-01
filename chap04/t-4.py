from core.Base import Base
from core.Mesh import Mesh
from core.Matrix import Matrix
from core.Renderer import Renderer
from core.Camera import Camera

from geometries.BoxGeometry import BoxGeometry
from materials.surfaceMaterial import SurfaceMaterial

from OpenGL.GL import *

import pygame


class Graphics(Base):
    """Render 3D objects in the screen"""

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.moveAmount = self.deltaTime * 1.5

        self.renderer = Renderer()

        self.camera = Camera(angleOfView=60)
        self.camera.setPosition([0, 0, 4])

        geometry = BoxGeometry()
        geometry.countVertices()

        surface = SurfaceMaterial()
        surface.addUniform("bool", "useBaseColorOnly", False)
        surface.uniforms["useVertexColors"].data = True
        surface.uniforms["projectionMatrix"].data = self.camera.projectionMatrix

        surface.locateUniforms()

        self.mesh = Mesh(geometry, surface)

    def update(self):
        self.handleInput()

        self.camera.updateViewMatrix()
        self.renderer.render(self.mesh, self.camera)


        # if(self.timer > 3):
        #     self.running = False


    def handleInput(self):
        for key in self.input.keyPressedList:

            ## VIEW CAMERA TRANSLATIONS ##

            if key == "w":
                self.camera.translate(0, +self.moveAmount, 0, False)
            if key == "s":
                self.camera.translate(0, -self.moveAmount, 0, False)
            if key == "a":
                self.camera.translate(-self.moveAmount, 0, 0, False)
            if key == "d":
                self.camera.translate(+self.moveAmount, 0, 0, False)
            if key == "q":
                self.camera.translate(0, 0, +self.moveAmount, False)
            if key == "e":
                self.camera.translate(0, 0, -self.moveAmount, False)

            # GLOBAL TRANSLATION TO THE OBJECT ##

            if key == "up":
                 self.mesh.translate(0, self.moveAmount, 0, useLocalCoordinates = False)
            if key == "down":
                self.mesh.translate(0, -self.moveAmount, 0, useLocalCoordinates = False)
            if key == "left": 
                self.mesh.translate(-self.moveAmount, 0, 0, useLocalCoordinates = False)
            if key == "right":
                 self.mesh.translate(self.moveAmount, 0, 0, useLocalCoordinates = False)

        self.mesh.rotateX(self.deltaTime * 0.9)
        self.mesh.rotateY(self.deltaTime * 0.9)

        if any( x in self.input.keyPressedList for x in ["w", "a", "s", "d", "up", "down", "left", "right" ] ):
            print("CAMERA X={:.2f}; Y={:.2f}; Z={:.2f} || GLOBAL TRANSOFRM X={:.2f}; Y={:.2f}; Z={:.2f} ".format(
                  self.mesh.material.uniforms["viewMatrix"].data[0][3],
                  self.mesh.material.uniforms["viewMatrix"].data[1][3],
                  self.mesh.material.uniforms["viewMatrix"].data[2][3],
                  self.mesh.transform[0][3],
                  self.mesh.transform[1][3],
                  self.mesh.transform[2][3]
                ))



Graphics().run()
