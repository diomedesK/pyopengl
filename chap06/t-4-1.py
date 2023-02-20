from core.Base import Base
from core.Camera import Camera
from core.Scene import Scene
from core.Renderer import Renderer
from core.Mesh import Mesh
from core.Texture import Texture

from geometries.RectangleGeometry import RectangleGeometry
from geometries.SphereGeometry import SphereGeometry

from materials.PhongMaterial import PhongMaterial

from extras.MovementRig import MovementRig
from extras.GridHelper import GridHelper
from extras.DirectionalLightHelper import DirectionalLightHelper

from light.AmbientLight import AmbientLight
from light.PointLight import PointLight
from light.DirectionalLight import DirectionalLight

import math

class Executor(Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def initialize(self):
        self.camera = Camera()
        self.rig = MovementRig()
        self.scene = Scene()
        self.renderer = Renderer(clearColor=[0.1 for n in range(4)]) #color aint working rn

        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 3])
        self.camera.setPosition([0, 0, 0])
        
        self.ambientLight = AmbientLight(color=[ 0.5 for n in range(3) ])
        self.directionalLight = DirectionalLight(color=[0.5, 0.5, 0.5], direction=[-1, -1, 0])
        self.directionalLight.setPosition([2, 5, 2])

        self.directionalLight.add(DirectionalLightHelper(self.directionalLight))

        ## SOME SETTINGS

        self.renderer.enableShadows(self.directionalLight)

        ## SET UP PRIMARY OBJECTS

        phong = PhongMaterial(
                texture=Texture("./images/grid_enum.jpg"), 
                numberOfLights=2,
                useShadow=True
                )

        phong.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0] )
        phong.locateUniforms()


        self.sphere = Mesh( SphereGeometry(radius=1), phong )
        self.sphere.setPosition([0, 1, 0]);

        self.ground = Mesh( SphereGeometry(radius = 10), phong )
        self.ground.rotateX(math.radians(90))

        self.ground.setPosition([0, 0, 0])
        
        
        # SET UP SECONDARY OBJECTS

        self.gridHelper = GridHelper(10, 10, color = [0, 0, 0], lineWidth=2)
        self.gridHelper.rotateX(math.radians(90))


        # ADD OBJECTS TO THE SCENE
        self.scene.add(self.rig)
        self.scene.add(self.ambientLight)
        self.scene.add(self.directionalLight)
        # self.scene.add(self.gridHelper)
        self.scene.add(self.sphere)
        self.scene.add(self.ground)
        
        
    def update(self):
        self.rig.update(self.input, self.deltaTime * 2)
        self.renderer.render(self.scene, self.camera)

        self.directionalLight.rotateY(0.01337, False)
        self.directionalLight.lookAt(self.sphere.getPosition())

Executor(screenSize=[600, 600], lockMouse = True).run()
