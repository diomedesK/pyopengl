from core.Base import Base
from core.Mesh import Mesh
from core.Matrix import Matrix
from core.Renderer import Renderer
from core.Camera import Camera
from core.Scene import Scene

from extras.MovementRig import MovementRig

from geometries.BoxGeometry import BoxGeometry
from materials.SurfaceMaterial import SurfaceMaterial

from OpenGL.GL import *

import math

debug = False

class Graphics(Base):
    """Render 3D objects in the screen"""

    def __init__(self):
        super().__init__(screenSize=(512, 512))

    def initialize(self):
        self.moveAmount = self.deltaTime * 1.5

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(angleOfView=60)
        self.rig = MovementRig()
        
        self.camera.setPosition([0, 0, 8])
        self.rig.add(self.camera)

        geometry = BoxGeometry()
        geometry.countVertices()

        surface = SurfaceMaterial()
        surface.addUniform("bool", "useBaseColorOnly", False)
        surface.uniforms["useVertexColors"].data = True
        surface.locateUniforms()

        self.scene.add(Mesh(geometry, surface) )
        self.scene.add(self.rig)

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

        mesh.rotateX(self.deltaTime * 0.9)
        mesh.rotateY(self.deltaTime * 0.9)
        

Graphics().run()
# main()
