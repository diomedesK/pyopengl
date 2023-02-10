from core.Object3D import Object3D
from core.Matrix import Matrix

import numpy

class Camera(Object3D):
    """View object for the 3D graphics"""
    def __init__(self, angleOfView=60, aspectRatio=1.0, near=0.1, far=1000):
        super(Camera, self).__init__()
        
        self.projectionMatrix = Matrix.makePerspective(angleOfView, aspectRatio, near, far)
        self.viewMatrix = Matrix.makeIdentity()

    def updateViewMatrix(self):
        self.viewMatrix = numpy.linalg.inv(self.getWorldTransform())

    def setPerspective(self, angleOfView=60, aspectRatio=1.0, near=0.1, far=1000):
        self.projectionMatrix = Matrix.makePerspective(angleOfView, aspectRatio, near, far)

    def setOrthographic(self, left = -1, right = 1, bottom = -1, top = 1, near = -1, far = 1):
        self.projectionMatrix = Matrix.makeOrthographic(left, right, bottom, top, near, far)
