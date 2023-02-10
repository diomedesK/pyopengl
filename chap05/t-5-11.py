from core.Base import Base
from core.Scene import Scene
from core.Mesh import Mesh
from core.Texture import Texture
from core.Renderer import Renderer
from core.Camera import Camera
from core.rendererTarget import RenderTarget

from extras.MovementRig import MovementRig

from materials.TextureMaterial import TextureMaterial
from geometries.RectangleGeometry import RectangleGeometry
from geometries.SphereGeometry import SphereGeometry
from geometries.BoxGeometry import BoxGeometry

from materials.SurfaceMaterial import SurfaceMaterial

import math

class Graphics(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initialize(self):
        self.moveAmout = self.deltaTime * 10

        self.scene =Scene()
        self.renderer = Renderer()
        self.rig = MovementRig()
        self.camera = Camera()
        self.skyCamera = Camera()

        self.skyCamera.setPosition([ 0, 30, 5 ])
        self.skyCamera.rotateX(math.radians(-80))

        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 5])

        # Default scenario
        planeGeo = RectangleGeometry(100, 100)
        planeMat = TextureMaterial(Texture("./images/grass.png"), {
            "repeatUV": [50, 50]
            })

        sphereGeo = SphereGeometry(100)
        sphereMat = TextureMaterial(Texture("./images/sky-earth.png"))

        self.floorMesh = Mesh(planeGeo, planeMat)
        self.floorMesh.rotateX( math.radians(90) )
        self.skyMesh = Mesh(sphereGeo, sphereMat)

        # Add tools for visualizing 

        self.virtualRenderingTarget = RenderTarget(resolution=[512, 512])
        self.frameMesh = Mesh(BoxGeometry(width=10, height=10), TextureMaterial(self.virtualRenderingTarget.texture )) 
        self.frameMesh.setPosition([0.9, 0.9, -8])

        self.sphereMesh = Mesh( SphereGeometry(2), TextureMaterial(Texture("./images/brick-color.png")) )
        self.sphereMesh.setPosition([ -10, 2, -6 ])
        
        self.characterMesh = Mesh( SphereGeometry(1/2), SurfaceMaterial())
        self.characterMesh.material.addUniform("vec3", "baseColor", [1.0, 0.0, 0.0])
        self.characterMesh.material.locateUniforms()
        
        self.scene.add(self.skyMesh)
        self.scene.add(self.floorMesh)
        self.scene.add(self.frameMesh)
        self.scene.add(self.sphereMesh)
        self.scene.add(self.characterMesh)
        self.scene.add(self.rig)

    def update(self):
        self.rig.update(self.input, self.moveAmout)
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(self.scene, self.skyCamera, renderTarget=self.virtualRenderingTarget)

        self.sphereMesh.rotateY(self.deltaTime)
        
        self.characterMesh.setPosition( self.rig.getPosition() )

        pass

Graphics(screenSize=[800, 600], lockMouse=True).run()
