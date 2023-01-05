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
        super().__init__(screenSize=(682, 682))

    def initialize(self):
        self.moveAmount = self.deltaTime * 1.5

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(angleOfView=60, far=50)
        self.rig = MovementRig()
        
        self.camera.setPosition([0, 2, 8])
        self.rig.add(self.camera)

        ## INITIALIZE GRID PLANE ##
        self.gridMesh = GridHelper(divisions=100, size=100)
        self.gridMesh.rotateX(-math.radians(90))

        ## INITIALIZE XYZ COORDINATES AT ORIGIN
    
        self.coordMesh = AxesHelper(lineWidth=10)

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

        self.getTurnAmount = lambda coef : coef * math.radians( self.deltaTime * 8 )
        self.input.onMouseMotion = lambda event: (
                self.camera.rotateY( self.getTurnAmount( -event.rel[0]) * 1),
                self.camera.rotateX( self.getTurnAmount( -event.rel[1]) * 1)
                )


    def update(self):
        self.renderer.render(self.scene, self.camera, self.meshHandler)
        self.rig.update(self.input, self.moveAmount)


    def meshHandler(self, mesh):
        for key in self.input.keyPressedList:
            ## GLOBAL TRANSLATION TO THE OBJECT ##
            if key == "up":
                mesh.translate(0, self.moveAmount, 0 )
            if key == "down":
                mesh.translate(0, -self.moveAmount, 0 )
            if key == "left": 
                mesh.translate(-self.moveAmount, 0, 0 )
            if key == "right":
                mesh.translate(self.moveAmount, 0, 0 )

        if mesh.id == "box":
            mesh.rotateX(self.deltaTime * 0.9)
            mesh.rotateY(self.deltaTime * 0.9)

Graphics().run()
# main()

