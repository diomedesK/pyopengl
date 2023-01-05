from core.Object3D import Object3D
from core.Matrix import Matrix

import numpy

class Camera(Object3D):
    """View object for the 3D graphics"""
    def __init__(self, angleOfView=60, aspectRatio=1, near=0.1, far=1000):
        super(Camera, self).__init__()
        
        self.viewMatrix = Matrix.makeIdentity()
        self.projectionMatrix = Matrix.makePerspective(angleOfView, aspectRatio, near, far)

        self.angleX, self.angleY = 0, 0

    def updateViewMatrix(self):
        self.viewMatrix = numpy.linalg.inv(self.getWorldTransform())

        pass
    
    def rotateX(self, angle, useLocalCoordinates = True):
        super(Camera, self).rotateX(angle, useLocalCoordinates)
        self.angleY += angle

        # print(angle)


    def rotateY(self, angle, useLocalCoordinates = True):
        super(Camera, self).rotateY(angle, useLocalCoordinates)
        self.angleX += angle
