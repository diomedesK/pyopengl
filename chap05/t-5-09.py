from core.Base import Base
from core.Mesh import Mesh
from core.Camera import Camera
from core.Scene import Scene
from core.Renderer import Renderer
from core.Texture import Texture

from extras.MovementRig import MovementRig
from extras.GridHelper import GridHelper

from extras.TextTexture import TextTexture
from materials.TextureMaterial import TextureMaterial

from geometries.RectangleGeometry import RectangleGeometry
from geometries.BoxGeometry import BoxGeometry

from OpenGL.GL import *
import time, math, numpy

class Graphics(Base):
    """Use dual scenes for billboarding"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
    
    def initialize(self):

        ## DEFAULT INIT 
        self.moveAmount = self.deltaTime* 10;

        self.scene = Scene()
        self.camera = Camera(aspectRatio=8/6)
        self.renderer = Renderer()
        self.viewRig = MovementRig()

        self.billboardingScene = Scene()
        self.billboardingCamera = Camera()

        self.billboardingCamera.setOrthographic(0, 800, 0, 600, 1, -1)

        ## ADD OBJECTS TO STANDARD SCENE

        self.gridHelper = GridHelper(divisions=500, size=500)
        self.gridHelper.rotateX(3.14 * 90 / 180)

        self.viewRig.add(self.camera)
        self.viewRig.setPosition([0, 2, 3])
        
        crateGeo = BoxGeometry()
        crateMat = TextureMaterial( Texture("./images/crate.png", {
            "magFilter": GL_LINEAR,
            "minFilter": GL_LINEAR,
            }))

        self.crateMesh = Mesh(crateGeo, crateMat)
        self.crateMesh.translate(5, 1/2, 0)

        self.scene.add(self.viewRig)
        self.scene.add(self.gridHelper)
        self.scene.add(self.crateMesh)

        ## ADD OBJECTS TO BILLBOARDING SCENE

        labelGeo1 = RectangleGeometry(width=800, height=600, position=[0, 0], alignment=[0,0])
        labelText1 = TextTexture("MyBillboardingMessage", transparent=True, fontColor=[255, 255, 1], fontSize=16, imageWidth=900, imageHeight=900)
        labelMat1 = TextureMaterial(labelText1)
        label1 = Mesh(labelGeo1, labelMat1)
        
        self.billboardingScene.add(label1)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(self.billboardingScene, self.billboardingCamera, clearColor = False)
        self.viewRig.update(self.input, self.moveAmount)

        self.crateMesh.rotateX( self.deltaTime )
        self.crateMesh.rotateY( self.deltaTime )

Graphics(screenSize=[800, 600], lockMouse=True).run()
