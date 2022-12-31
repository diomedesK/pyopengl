from core.Matrix import Matrix

# 1. a matrix to store its transform data
# 2. a list of references to child objects
# 3. a reference to a parent object

class Object3D(object):
    """ A node in the scene graph """

    def __init__(self):
        # the transform matrix here is equivalent to the model matrix of previous lessons
        self.transform = Matrix.makeIdentity() 

        self.parent = None
        self.children = []
        pass

    def add(self, child):
        self.children.append(child)
        child.parent = self
        pass

    def remove(self, child):
        self.children.remove(child)
        child.parent = None
        pass

    #calculate transformation on this object3D relative # to the root object3D of the scene graph
    def getWorldMatrix(self):
        if self.parent == None:
            return self.transform
        else:
            return self.parent.getWorldMatrix() @ self.transform


    def getDescendantsList(self):
        descendants = []
        nodesToProcess = [self]

        while len(nodesToProcess) > 0:
            node = nodesToProcess.pop()
            descendants.append(node)
            nodesToProcess = node.children + nodesToProcess

        return descendants

    def applyMatrix(self, matrix, localCoordinates=True):
        if localCoordinates:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform 
    
    def translate(self, x, y, z, localCoordinates = True):
        m = Matrix.makeTranslation(x, y, z)
        self.applyMatrix( m, localCoordinates )

    def rotateX(self, angle, localCoordinates = True):
        m = Matrix.makeRotationX(angle)
        self.applyMatrix(m, localCoordinates)
        pass

    def rotateY(self, angle, localCoordinates = True):
        m = Matrix.makeRotationY(angle)
        self.applyMatrix(m, localCoordinates)
        pass

    def rotateZ(self, angle, localCoordinates = True):
        m = Matrix.makeRotationZ(angle)
        self.applyMatrix(m, localCoordinates)
        pass

    def scale(self, coefficient, localCoordinates = True):
        m = Matrix.makeScale(coefficient)
        self.applyMatrix(m, localCoordinates)

    def getPosition(self):
        return [ 
                self.transform.item((0, 3)),
                self.transform.item((1, 3)),
                self.transform.item((2, 3)),
                ]
    
    def getWorldPosition(self):
        worldTransform = self.getWorldMatrix()
        return [ 
                worldTransform.item((0, 3)),
                worldTransform.item((1, 3)),
                worldTransform.item((2, 3)),
                ]

    def setPosition(self, position):
        return [ 
                self.transform.itemset((0, 3), position[0]),
                self.transform.itemset((1, 3), position[1]),
                self.transform.itemset((2, 3), position[2]),
                ]
