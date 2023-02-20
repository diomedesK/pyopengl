from core.Camera import Camera
from core.RendererTarget import RenderTarget

from materials.DepthMaterial import DepthMaterial
from OpenGL.GL import *

class Shadow(object):
    def __init__(self, lightSource, strength=0.5, 
                 resolution=[512, 512],
                 cameraBounds = [-5, 5, -5, 5, 0, 20], 
                 bias = 0.01
                 ):

        super().__init__()

        self.camera = Camera()
        self.lightSource = lightSource
        
        left, right, bottom, top, near, far = cameraBounds
        self.camera.setOrthographic( left, right, bottom, top, near, far  )
        self.lightSource.add(self.camera)

        # fix 'properties' param in RendererTarget
        self.renderTarget = RenderTarget(resolution, 
                                         properties={
                                             "wrap": GL_CLAMP_TO_BORDER
                                             })
        self.material = DepthMaterial()

        self.strength = strength
        self.bias = bias


    def updateInternal(self):
        self.camera.updateViewMatrix()
        self.material.uniforms["viewMatrix"].data = self.camera.viewMatrix
        self.material.uniforms["projectionMatrix"].data = self.camera.projectionMatrix
