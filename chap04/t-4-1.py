from core.Base import Base
from core.Uniform import Uniform
from core.Object3D import Object3D
from core.Mesh import Mesh
from core.Renderer import Renderer

from core.Scene import Scene
from core.Camera import Camera


from materials.SurfaceMaterial import SurfaceMaterial 
from geometries.BoxGeometry import BoxGeometry

from core.OpenGLUtils import OpenGLUtils

class Test(Base):

    def initialize(self):
        print("Initializing program")

        self.renderer = Renderer()
        self.camera = Camera(aspectRatio=(800/600))
        self.scene = Scene()

        self.camera.setPosition([0, 0, 4])

        geometry = BoxGeometry()
        material = SurfaceMaterial({"useVertexColors": True})

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

        pass

    def update(self):
        self.mesh.rotateY( 0.05 )
        self.mesh.rotateX( 0.03 )
        self.renderer.render(self.scene, self.camera)


Test().run()
