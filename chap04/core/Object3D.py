from core.Matrix import Matrix

class Object3D(object):
    """A node in the scene graph, with functions handling common usage"""
    def __init__(self):
        super(Object3D, self).__init__()
        self.parent = None
        self.children = None
        self.transform = Matrix.makeIdentity()
    

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
