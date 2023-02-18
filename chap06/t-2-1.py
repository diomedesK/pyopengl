from core.Base import Base
from core.Camera import Camera
from core.Scene import Scene
from core.Renderer import Renderer
from core.Mesh import Mesh
from core.Texture import Texture

from geometries.RectangleGeometry import RectangleGeometry

from materials.LambertMaterial import LambertMaterial

from extras.MovementRig import MovementRig
from extras.PointLightHelper import PointLightHelper
from extras.GridHelper import GridHelper

from light.AmbientLight import AmbientLight
from light.PointLight import PointLight

import math

class Executor(Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def initialize(self):
        self.camera = Camera()
        self.rig = MovementRig()
        self.scene = Scene()
        self.renderer = Renderer()

        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 3])
        self.camera.setPosition([0, 0, 0])
        
        self.ambientLight = AmbientLight(color=[ 0.5 for n in range(3) ])
        self.pointLight = PointLight(color=[0.9, 0, 0], position=[0, 0, 0])
        
        # SET UP BRICK WALL

        wallGeometry = RectangleGeometry(width=2, height=2)
        bumpMaterial = LambertMaterial( 
                                       numberOfLights=4,
                                       texture = Texture("./images/brick-color.png"),
                                       bumpTexture=Texture("./images/brick-bump.png")
                                       )

        self.brickWall = Mesh(wallGeometry, bumpMaterial)
        self.brickWall.setPosition([0, 1, 0])

        if not "baseColor" in self.brickWall.material.uniforms.keys():
            self.brickWall.material.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.brickWall.material.locateUniforms()

        # SET UP SECONDARY OBJECTS

        self.gridHelper = GridHelper(10, 10)
        self.gridHelper.rotateX(math.radians(90))

        self.pointLightHelper = PointLightHelper(self.pointLight)
        self.pointLight.add(self.pointLightHelper)
        self.pointLight.setPosition([2, 1, 1])

        self.scene.add(self.pointLight)

        # ADD OBJECTS TO THE SCENE
        self.scene.add(self.rig)
        self.scene.add(self.ambientLight)
        
        self.scene.add(self.gridHelper)
        self.scene.add(self.brickWall)
        
    def update(self):
        self.rig.update(self.input, self.deltaTime * 2)
        self.renderer.render(self.scene, self.camera)
        
        # self.pointLight.translate(math.sin(self.timer + 1.5) /6, 0, 0)
        # print(self.pointLightHelper.getWorldPosition())



Executor(screenSize=[600, 600], lockMouse = True).run()
