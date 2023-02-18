from core.Base import Base
from core.Camera import Camera
from core.Scene import Scene
from core.Renderer import Renderer
from core.Mesh import Mesh
from core.Texture import Texture

from geometries.SphereGeometry import SphereGeometry
from geometries.RectangleGeometry import RectangleGeometry

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
        
        self.customObjects = []

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

        customObjectFlat = Mesh(sphereGeometry, flatMaterial)
        customObjectFlat.setPosition([-2.2, 1.0, 0])

        customObjectLambert = Mesh(sphereGeometry, lambertMaterial)
        customObjectLambert.setPosition([0, 1.0, -2])
        customObjectLambert.material.addUniform("vec3", "baseColor", [ 1.0, 1.0, 1.0 ])

        customObjectPhong = Mesh(sphereGeometry, phongMaterial)
        customObjectPhong.setPosition([2.2, 1.0, 0])
        customObjectPhong.material.addUniform("vec3", "baseColor", [ 0.5, 0.5, 0.5 ])

        brickGeometry = RectangleGeometry(width=2, height = 2)
        bumpMaterial = LambertMaterial( 
                                       numberOfLights=4,
                                       texture = Texture("./images/brick-color.png"),
                                       bumpTexture=Texture("./images/brick-bump.png")
                                       )
        customObjectBrick = Mesh(brickGeometry, bumpMaterial)
        customObjectBrick.setPosition([0.0, 1.0, 0])
        customObjectBrick.material.addUniform("vec3", "baseColor", [ 1.0 for n in range(3) ])
        customObjectBrick.id = "brick"

        self.customObjects.extend([
            customObjectFlat, 
            customObjectLambert,
            customObjectPhong,
            customObjectBrick
            ])

        for customObject in self.customObjects:
            if not "baseColor" in customObject.material.uniforms.keys():
                customObject.material.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])

            customObject.material.locateUniforms()
            self.scene.add(customObject)
        
        ## ADD OBJECTS TO SCENE
        self.gridObject = GridHelper()
        self.gridObject.rotateX(math.radians(90))

        self.directionalLightHelper = DirectionalLightHelper(self.directionalLight)
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

        for customObject in self.customObjects:
            if customObject.id == "brick":
                continue

            customObject.rotateY(self.deltaTime)

        self.directionalLight.setDirection( [ -1, math.sin(0.7*self. timer), -2] )
        self.pointLight1.translate(math.sin(self.timer + 1.5) /6, 0, 0)

Executor(screenSize=[600, 600], lockMouse = True).run()
