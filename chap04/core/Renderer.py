from core.Matrix import Matrix
from core.Mesh import Mesh
from OpenGL.GL import *

import numpy, pygame




class Renderer(object):
    """docstring for Renderer"""
    def __init__(self):
        super(Renderer, self).__init__()

        # setup settings
        glPointSize(10)
        glLineWidth(5)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClearColor(1, 1, 1, 1);

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 

        self.meshFilter = lambda x : isinstance(x, Mesh)


    def render(self, scene, camera, meshHandler):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) #pyright: ignore

        meshList = list(filter(self.meshFilter, scene.getDescendantsList()))

        for mesh in meshList:
            meshHandler(mesh)

            glUseProgram(mesh.material.program)

            glBindVertexArray(mesh.VAO)
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["modelMatrix"].data = mesh.transform
            
            for uniformName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
                pass

            for attributeName, attributeObject in mesh.geometry.attributes.items():
                attributeObject.uploadData()

            glDrawArrays( GL_TRIANGLES, 0, mesh.geometry.vertexCount )
            
            #mesh.material.updateRenderSettings() 

