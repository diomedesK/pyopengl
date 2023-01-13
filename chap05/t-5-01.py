from core.Base import Base
from core.Texture import Texture
from core.Mesh import Mesh
from core.Renderer import Renderer
from core.Scene import Scene
from core.Camera import Camera

from geometries.RectangleGeometry import RectangleGeometry
from materials.TextureMaterial import TextureMaterial

import math

class Graphics(Base):
    """Graphics object"""
    def __init__(self):
        super(Graphics, self).__init__()
    
    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera()
        self.camera.setPosition([0, 0, 2])

        text = Texture("./images/grid.png")
        surface = TextureMaterial(text)
        geometry = RectangleGeometry()

        self.mesh = Mesh(geometry, surface)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        if self.timer > 8:
            self.running = False;

        self.mesh.rotateX(self.deltaTime * math.sin(self.timer))
        self.mesh.rotateY(self.deltaTime * math.sin(self.timer))
        self.mesh.rotateZ(self.deltaTime * math.sin(self.timer))

Graphics().run()
