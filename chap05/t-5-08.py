from core.Base import Base
from core.Mesh import Mesh
from core.Camera import Camera
from core.Scene import Scene
from core.Renderer import Renderer
from core.Texture import Texture

from extras.MovementRig import MovementRig
from extras.GridHelper import GridHelper

from materials.SpriteMaterial import SpriteMaterial
from materials.SurfaceMaterial import SurfaceMaterial

from geometries.RectangleGeometry import RectangleGeometry

from OpenGL.GL import *
import time, math, numpy

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

        texture = Texture("./images/rolling-ball.png")
        targetMat = SpriteMaterial(texture, {
            "billboard" : 1,
            "tileCount" : [8, 4],
            "tileNumber": 0
                                       })
        targetGeo = RectangleGeometry()

        self.mesh = Mesh(targetGeo, targetMat)

        self.gridHelper = GridHelper(divisions=500, size=500)
        self.gridHelper.rotateX(3.14 * 90 / 180)
        
        self.viewRig.add(self.camera)
        self.viewRig.setPosition([0, 2, 3])

        self.scene.add(self.gridHelper)
        self.scene.add(self.viewRig)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.viewRig.update(self.input, self.moveAmount)

        tileNumber = math.floor(self.timer * 8)
        self.mesh.material.uniforms["tileNumber"].data = tileNumber

    def main(self):
        pass
    

Graphics(lockMouse=True).run()
