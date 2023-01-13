from core.Base import Base
from core.Mesh import Mesh
from core.Camera import Camera
from core.Scene import Scene
from core.Renderer import Renderer

from extras.MovementRig import MovementRig

from extras.TextTexture import TextTexture
from extras.GridHelper import GridHelper

from materials.TextureMaterial import TextureMaterial
from materials.LineMaterial import LineMaterial
from materials.SurfaceMaterial import SurfaceMaterial

from geometries.BoxGeometry import BoxGeometry
from geometries.RectangleGeometry import RectangleGeometry

from OpenGL.GL import *

import numpy, math

class Graphics(Base):
    """Apply billboarding based on matrix tranformation to object"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
    
    def initialize(self):
        self.moveAmount = self.deltaTime* 10;

        self.scene = Scene()
        self.camera = Camera()
        self.renderer = Renderer()
        self.viewRig = MovementRig()


        self.controlRig = MovementRig( userDefinedControls={
                "front"    : "up",
                "back"  : "down",
                "left"  : "left",
                "right" : "right",
                "up": "u",
                "down" : "i",
                })

        self.viewRig.add(self.camera)

        # self.viewRig.setPosition([0, 0, 0])
        self.camera.setPosition([ 0, 0, 25 ])

        ## initialize box mesh
        
        planeGeo = RectangleGeometry()
        message = TextTexture( imageWidth=256, imageHeight=256, alignHorizontal=1/2, alignVertical=1/2)
        planeMat = TextureMaterial(message)

        self.planeMesh = Mesh(planeGeo, planeMat)
        self.planeMesh.translate(0, 1/2, 0)

        self.boxMesh = Mesh(BoxGeometry(), SurfaceMaterial(
            {"baseColor": [1, 0, 0]}
            ))
        self.controlRig.translate(-math.radians(360), 0.00, -math.radians(360))

        self.gridMesh = GridHelper(divisions=500, size=500)
        self.gridMesh.rotateX( 3.14 * 90 /180 )

        ## Add the objects to the scene

        self.scene.add(self.gridMesh)
        self.scene.add(self.viewRig)
        self.scene.add(self.boxMesh)
        self.scene.add(self.planeMesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)

        self.viewRig.update(self.input, self.moveAmount)
        self.controlRig.update(self.input, self.moveAmount)

        self.boxMesh.setPosition(self.controlRig.getPosition())

        # mX = math.cos(self.timer) * 0.2
        # mY = math.sin(self.timer) * 0.2
        # # print(mX)
        # self.controlRig.translate(mX, 0, mY)

        self.planeMesh.lookAt(
                self.camera.getWorldPosition()
                )

Graphics(lockMouse=True).run()

