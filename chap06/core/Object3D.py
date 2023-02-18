from core.Matrix import Matrix
from typing import Union
import numpy

class Object3D(object):
    """A node in the scene graph, with functions handling common usage"""

    def __init__(self):
        self.parent = None 
        self.children = []
        self.transform = Matrix.makeIdentity()
        self.id: Union[str, None] = None

    def add(self, child):
        self.children.append(child)
        child.parent = self
    
    def remove(self, child):
        self.children.remove(child)
        child.parent = None

    def getDescendantsList(self):
        descendants = []
        nodesToProcess = [self]

        while len(nodesToProcess) > 0:
            node = nodesToProcess.pop(0)
            descendants.append(node)

            nodesToProcess = node.children + nodesToProcess

        return descendants

    def getWorldTransform(self): #not equal to a "getGlobalTransform"
        if self.parent == None:
            return self.transform
        else:
            return self.parent.getWorldTransform() @ self.transform

    def getWorldPosition(self):
        worldTransform = self.getWorldTransform()
        return [
                worldTransform.item((0, 3)),
                worldTransform.item((1, 3)),
                worldTransform.item((2, 3)),
                ]

    def applyMatrix(self, matrix, useLocalCoordinates = True):
        if useLocalCoordinates:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform 
    
    def rotateX(self, angle, useLocalCoordinates = True):
        m = Matrix.makeRotationX(angle)
        self.applyMatrix(m, useLocalCoordinates)
        pass

    def rotateY(self, angle, useLocalCoordinates = True):
        m = Matrix.makeRotationY(angle)
        self.applyMatrix(m, useLocalCoordinates)
        pass

    def rotateZ(self, angle, useLocalCoordinates = True):
        m = Matrix.makeRotationZ(angle)
        self.applyMatrix(m, useLocalCoordinates)
        pass

    def translate(self, x, y, z, useLocalCoordinates = True):
        m = Matrix.makeTranslation(x, y, z)
        self.applyMatrix(m, useLocalCoordinates)

    def scale(self, size, useLocalCoordinates = True):
        m = Matrix.makeScale(size)
        self.applyMatrix(m, useLocalCoordinates)

    def getRotationMatrix(self):
        return numpy.array(
            [
                self.transform[0][0:3],
                self.transform[1][0:3],
                self.transform[2][0:3]
            ]
        )

    def getDirection(self):
        forward = numpy.array([0,0,-1])
        return list(self.getRotationMatrix() @ forward)

    def setDirection(self, direction):
        position = self.getPosition()
        targetPosition = [ position[0] + direction[0],
        position[1] + direction[1],
        position[2] + direction[2] ]
        self.lookAt( targetPosition )

    def getPosition(self):
        return [
                self.transform.item((0, 3)),
                self.transform.item((1, 3)),
                self.transform.item((2, 3)),
                ]

    def setPosition(self, position):
        p = position
        return [
                self.transform.itemset( (0, 3), p[0] ),
                self.transform.itemset( (1, 3), p[1] ),
                self.transform.itemset( (2, 3), p[2] ),
                ]

    def lookAt(self, targetPosition):
        m = Matrix.makeLookAt(self.getWorldPosition(), targetPosition)
        self.transform = m
