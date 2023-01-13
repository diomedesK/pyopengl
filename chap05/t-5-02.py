from core.Base import Base
from core.Scene import Scene
from core.Mesh import Mesh
from core.Texture import Texture
from core.Renderer import Renderer
from core.Camera import Camera
from extras.MovementRig import MovementRig

from materials.TextureMaterial import TextureMaterial
from geometries.RectangleGeometry import RectangleGeometry
from geometries.SphereGeometry import SphereGeometry

import math

class Graphics(Base):
    def __init__(self):
        super(Graphics, self).__init__()

    def initialize(self):
        self.moveAmout = self.deltaTime * 10

        self.scene =Scene()
        self.renderer = Renderer()
        self.rig = MovementRig()
        self.camera = Camera()

        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 5])

        planeGeo = RectangleGeometry(100, 100)
        planeMat = TextureMaterial(Texture("./images/grass.png"), {
            "repeatUV": [50, 50]
            })

        sphereGeo = SphereGeometry(100)
        sphereMat = TextureMaterial(Texture("./images/sky-earth.png"))

        self.floorMesh = Mesh(planeGeo, planeMat)
        self.floorMesh.rotateX( math.radians(90) )

        self.skyMesh = Mesh(sphereGeo, sphereMat)

        self.scene.add(self.skyMesh)
        self.scene.add(self.floorMesh)
        self.scene.add(self.rig)
    

    def update(self):
        self.rig.update(self.input, self.moveAmout)
        self.renderer.render(self.scene, self.camera)
        pass

Graphics().run()
