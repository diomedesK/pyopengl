from core.Base import Base
from core.Camera import Camera
from core.Scene import Scene
from core.Renderer import Renderer
from core.Mesh import Mesh
from core.Texture import Texture

from geometries.SphereGeometry import SphereGeometry

from materials.FlatMaterial import FlatMaterial
from materials.LambertMaterial import LambertMaterial
from materials.PhongMaterial import PhongMaterial
from materials.SurfaceMaterial import SurfaceMaterial

from extras.MovementRig import MovementRig
from extras.GridHelper import GridHelper
from extras.DirectionalLightHelper import DirectionalLightHelper
from extras.PointLightHelper import PointLightHelper

from light.Light import Light
from light.AmbientLight import AmbientLight
from light.DirectionalLight import DirectionalLight
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
        self.rig.setPosition([0, 2, 8])
        self.camera.setPosition([0, 0, 0])
        
        self.sphereObjects = []

        self.ambientLight = AmbientLight(color=[ 0.1 for n in range(3) ])
        self.directionalLight = DirectionalLight(color=[0.8, 0.8, 0.8], direction=[-1, -1, -2])
        self.pointLight1 = PointLight(color=[0.9, 0, 0], position=[0, 0, 0])
        self.pointLight2 = PointLight(color=[0, 0.9, 0], position=[-4, 0, 0])
        
        flatMaterial = FlatMaterial(
                texture=Texture("./images/grid_enum.jpg"),
                numberOfLights=4)

        lambertMaterial = LambertMaterial(
                numberOfLights=4)

        phongMaterial = PhongMaterial(
                numberOfLights=4)

        ## SET-UP SPHERES
        sphereGeometry = SphereGeometry(1)

        sphereObjectFlat = Mesh(sphereGeometry, flatMaterial)
        sphereObjectFlat.setPosition([-2.2, 1.0, 0])

        sphereObjectLambert = Mesh(sphereGeometry, lambertMaterial)
        sphereObjectLambert.setPosition([0, 1.0, 0])
        sphereObjectLambert.material.addUniform("vec3", "baseColor", [ 1.0, 1.0, 1.0 ])

        sphereObjectPhong = Mesh(sphereGeometry, phongMaterial)
        sphereObjectPhong.setPosition([2.2, 1.0, 0])
        sphereObjectPhong.material.addUniform("vec3", "baseColor", [ 0.5, 0.5, 0.5 ])

        self.sphereObjects.extend([
            sphereObjectFlat, 
            sphereObjectLambert,
            sphereObjectPhong
            ])

        for sphereObject in self.sphereObjects:
            if not "baseColor" in sphereObject.material.uniforms.keys():
                sphereObject.material.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])

            sphereObject.material.locateUniforms()
            self.scene.add(sphereObject)
        
        ## ADD OBJECTS TO SCENE
        self.gridObject = GridHelper()
        self.gridObject.rotateX(math.radians(90))

        self.directionalLightHelper = DirectionalLightHelper(self.pointLight1)
        self.directionalLight.add(self.directionalLightHelper)
        self.directionalLight.setPosition([2, 5, 0])

        self.pointLightHelper = PointLightHelper(self.pointLight1)
        self.pointLight1.add(self.pointLightHelper)
        self.pointLight1.setPosition([2, 5, 0])

        self.scene.add(self.pointLight1)
        self.scene.add(self.pointLight2)
        self.scene.add(self.ambientLight)
        self.scene.add(self.directionalLight)
        self.scene.add(self.rig)
        
        self.scene.add(self.gridObject)

    def update(self):
        self.rig.update(self.input, self.deltaTime * 2)
        self.renderer.render(self.scene, self.camera)

        for sphereObject in self.sphereObjects:
            sphereObject.rotateY(self.deltaTime)

        self.directionalLight.setDirection( [ -1, math.sin(0.7*self. timer), -2] )
        self.pointLight1.translate(math.sin(self.timer + 1.5) /6, 0, 0)

Executor(screenSize=[600, 600], lockMouse = True).run()
