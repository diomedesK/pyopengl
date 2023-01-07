from core.Base import Base
from core.Mesh import Mesh
from core.Matrix import Matrix
from core.Renderer import Renderer
from core.Camera import Camera
from core.Scene import Scene

from core.Geometry import Geometry
from materials.BasicMaterial import BasicMaterial

from materials.SurfaceMaterial import SurfaceMaterial
from geometries.BoxGeometry import BoxGeometry

from extras.MovementRig import MovementRig
from extras.GridHelper import GridHelper
from extras.AxesHelper import AxesHelper

from OpenGL.GL import *

import math

debug = False

class Graphics(Base):
    """Render 3D objects in the screen"""

    def __init__(self):
        super().__init__(screenSize=(1024, 1024))

    def initialize(self):
        self.moveAmount = self.deltaTime * 10

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(angleOfView=60, far=1000)
        self.rig = MovementRig(self.deltaTime)
        
        self.rig.add(self.camera)
        self.rig.setPosition([ 0, 2, 9 ])

        ## INITIALIZE GRID PLANE ##
        self.gridMesh = GridHelper(divisions=500, size=500)
        self.gridMesh.rotateX(-math.radians(90))

        ## INITIALIZE XYZ COORDINATES AT ORIGIN
    
        self.coordMesh = AxesHelper(axisLength=1000, lineWidth=5)

        ## INITIALIZE BOX OBJECT ##

        boxGeo = BoxGeometry()
        boxMat = SurfaceMaterial()

        boxMat.addUniform("bool", "useBaseColorOnly", False)
        boxMat.addUniform("bool", "useVertexColors", True)
        boxMat.locateUniforms()

        self.boxMesh = Mesh(boxGeo, boxMat)
        self.boxMesh.translate(2, 1.5, 2)
        self.boxMesh.id = "box"

        ## ADD OBJECTS TO THE SCENE ##
        self.scene.add(self.rig)
        self.scene.add(self.gridMesh)
        self.scene.add(self.coordMesh)
        self.scene.add(self.boxMesh)


        ## Functions and anonymous functions

    def update(self):
        self.renderer.render(self.scene, self.camera, self.meshHandler)
        self.rig.update(self.input, self.moveAmount)


    def meshHandler(self, mesh):
        if mesh.id == "box":
            mesh.rotateX(self.deltaTime * 0.9)
            mesh.rotateY(self.deltaTime * 0.9)

            for key in self.input.keyPressedList:
                ## GLOBAL TRANSLATION TO THE OBJECT ##
                if key == "up":
                    mesh.translate(0, self.moveAmount, 0, useLocalCoordinates = False)
                if key == "down":
                    mesh.translate(0, -self.moveAmount, 0, useLocalCoordinates = False )
                if key == "left": 
                    mesh.translate(-self.moveAmount, 0, 0, useLocalCoordinates = False )
                if key == "right":
                    mesh.translate(self.moveAmount, 0, 0, useLocalCoordinates = False )
                if key == "z": 
                    mesh.translate(0, 0, -self.moveAmount, useLocalCoordinates = False )
                if key == "x":
                    mesh.translate(0, 0, +self.moveAmount, useLocalCoordinates = False )

Graphics().run()
# main()

