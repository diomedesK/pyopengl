from core.Object3D import Object3D
from OpenGL.GL import *
from core.Attribute import Attribute

# Stores the geomtric and material data about a specific shape, 
# including a vertex array objec which also contains both

class Mesh(Object3D):
    """Stores geomtric and material data about a specific shape"""
    def __init__(self, geometry, material):
        super(Mesh, self).__init__()

        self.geometry = geometry
        self.material = material

        self.visible = True

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        glBindVertexArray(0)
