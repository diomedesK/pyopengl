
from core.Object3D import Object3D
from OpenGL.GL import *

class Mesh(Object3D):
    """docstring for Mesh"""
    def __init__(self, geometry, material):
        super(Mesh, self).__init__()

        self.geometry = geometry
        self.material = material

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        #link geometry's attribute data to program stored in the material instance
        for attributeName, attributeObject in self.geometry.attributes.items():
            attributeObject.associateVariable(self.material.program, attributeName)
        

        glBindVertexArray(0)

