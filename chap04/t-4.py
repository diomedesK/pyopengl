from core.Base import Base
from core.Mesh import Mesh
from core.Matrix import Matrix

from geometries.BoxGeometry import BoxGeometry
from materials.surfaceMaterial import SurfaceMaterial

from OpenGL.GL import *
import numpy, inspect

class Graphics(Base):
    """Render 3D objects in the screen"""

    def __init__(self):
        super().__init__()

    def initialize(self):
        glPointSize(10)
        glLineWidth(5)
        glEnable(GL_CULL_FACE)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        geometry = BoxGeometry()
        surface = SurfaceMaterial()

        geometry.countVertices()

        self.worldMatrix = Matrix.makeTranslation(0, 0, 0)

        surface.addUniform("bool", "useBaseColorOnly", False)

        surface.uniforms["projectionMatrix"].data = Matrix.makePerspective()
        surface.uniforms["viewMatrix"].data = numpy.linalg.inv(self.worldMatrix) @ Matrix.makeTranslation(0, 0, -4)
        surface.uniforms["modelMatrix"].data = Matrix.makeTranslation(0, 0, 0)
        surface.uniforms["useVertexColors"].data = True

        # The line below does not in this case, because the above variables are already built-in in the Material class, 
        # so when the Surface class calls locateUniforms at its end, they are located altogether. But it's a good practice
        # to keep it
        surface.locateUniforms()

        # geometry.attributes["vertexColor"].data = [0.5, 0.5, 0]

        self.mesh = Mesh(geometry, surface)

    
    def update(self):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) #pyright: ignore

        glUseProgram(self.mesh.material.program)
        glBindVertexArray(self.mesh.VAO)
        
        for uniformName, uniformObject in self.mesh.material.uniforms.items():
            uniformObject.uploadData()
            pass

        for attributeName, attributeObject in self.mesh.geometry.attributes.items():
            print(attributeName, attributeObject.data)
            attributeObject.uploadData()

        glDrawArrays( GL_TRIANGLES, 0, self.mesh.geometry.vertexCount )
        # glDrawArrays( self.mesh.material.settings["drawStyle"], 0, self.mesh.geometry.vertexCount )

        if(self.timer > 3):
            self.running = False

        pass

Graphics().run()

