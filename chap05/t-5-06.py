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

from geometries.BoxGeometry import BoxGeometry
from geometries.RectangleGeometry import RectangleGeometry

from OpenGL.GL import *

import numpy

class Graphics(Base):
    """Apply text textures to objects"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
    
    def initialize(self):
        self.moveAmount = self.deltaTime* 10;

        self.scene = Scene()
        self.camera = Camera()
        self.renderer = Renderer()
        self.rig = MovementRig()

        self.rig.add(self.camera)

        self.rig.setPosition([0, 2, 4])

        ## initialize box mesh
        
        planeGeo = RectangleGeometry()
        message = TextTexture( imageWidth=256, imageHeight=256, alignHorizontal=1/2, alignVertical=1/2)
        planeMat = TextureMaterial(message)

        self.planeMesh = Mesh(planeGeo, planeMat)
        self.planeMesh.translate(0, 1/2, 0)
        # self.planeMesh.rotateZ( 3.14 )

        self.gridMesh = GridHelper(divisions=500, size=500)
        self.gridMesh.rotateX( 3.14 * 90 /180 )

        # self.boxMesh.rotateY(3.14 * 45 /180)

        self.scene.add(self.rig)
        self.scene.add(self.gridMesh)
        self.scene.add(self.planeMesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.moveAmount)

        glMatrixMode(GL_TEXTURE)

Graphics(lockMouse=True).run()
