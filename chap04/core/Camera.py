from core.Object3D import Object3D
from core.Matrix import Matrix

import numpy

#The Camera has a projection and view matrix
class Camera(Object3D):
    """Stores data describing the visible region of the scene"""

    def __init__(self, angleOfView=60, aspectRatio=1.0, near=0.1, far=1000):
        super(Camera, self).__init__()

        self.projectionMatrix = Matrix.makePerspective(angleOfView, aspectRatio, near, far)
        self.viewMatrix = Matrix.makeIdentity()
    
    def updateViewMatrix(self):
        self.viewMatrix = numpy.linalg.inv(self.getWorldMatrix())
