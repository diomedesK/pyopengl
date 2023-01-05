from core.Base import Base
from core.Mesh import Mesh
from core.Matrix import Matrix
from core.Renderer import Renderer
from core.Camera import Camera
from core.Scene import Scene

from geometries.BoxGeometry import BoxGeometry
from materials.SurfaceMaterial import SurfaceMaterial

from OpenGL.GL import *

import pygame


debug = False

class Graphics(Base):
    """Render 3D objects in the screen"""

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.moveAmount = self.deltaTime * 1.5

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(angleOfView=60)

        self.camera.setPosition([0, 0, 4])

        geometry = BoxGeometry()
        geometry.countVertices()

        surface = SurfaceMaterial()
        surface.addUniform("bool", "useBaseColorOnly", False)
        surface.uniforms["useVertexColors"].data = True
        surface.uniforms["projectionMatrix"].data = self.camera.projectionMatrix

        surface.locateUniforms()
        self.scene.add( Mesh(geometry, surface) )

    def update(self):

        self.camera.updateViewMatrix()
        self.renderer.render(self.scene, self.camera, self.meshHandler)

        self.inputHandler()

        # if(self.timer > 3):
        #     self.running = False
    

    def meshHandler(self, mesh):
        for key in self.input.keyPressedList:
            ## GLOBAL TRANSLATION TO THE OBJECT ##
            if key == "up":
                mesh.translate(0, self.moveAmount, 0, useLocalCoordinates = False)
            if key == "down":
                mesh.translate(0, -self.moveAmount, 0, useLocalCoordinates = False)
            if key == "left": 
                mesh.translate(-self.moveAmount, 0, 0, useLocalCoordinates = False)
            if key == "right":
                mesh.translate(self.moveAmount, 0, 0, useLocalCoordinates = False)

        mesh.rotateX(self.deltaTime * 0.9)
        mesh.rotateY(self.deltaTime * 0.9)

    def inputHandler(self):
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


        # if debug and any( x in self.input.keyPressedList for x in ["w", "a", "s", "d", "up", "down", "left", "right" ] ):
            # print("CAMERA X={:.2f}; Y={:.2f}; Z={:.2f} || GLOBAL TRANSOFRM X={:.2f}; Y={:.2f}; Z={:.2f} ".format(
            #       self.mesh.material.uniforms["viewMatrix"].data[0][3],
            #       self.mesh.material.uniforms["viewMatrix"].data[1][3],
            #       self.mesh.material.uniforms["viewMatrix"].data[2][3],
            #       self.mesh.transform[0][3],
            #       self.mesh.transform[1][3],
            #       self.mesh.transform[2][3]
            #     ))


Graphics().run()
