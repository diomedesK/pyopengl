from core.Matrix import Matrix
from core.Mesh import Mesh
from OpenGL.GL import *

import numpy, pygame

debug = True

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

        # glClearColor(1, 1, 1, 1); #white bg
        glClearColor(0, 0, 0, 1); #black bg

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 

        self.meshFilter = lambda x : isinstance(x, Mesh)


    def render(self, scene, camera, meshHandler):
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) #pyright: ignore

        camera.updateViewMatrix()

        meshList = list(filter(self.meshFilter, scene.getDescendantsList()))

        for mesh in meshList:
            meshHandler(mesh)

            glUseProgram(mesh.material.program)

            glBindVertexArray(mesh.VAO)
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["modelMatrix"].data = mesh.transform
            
            for uniformName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
                pass

            for attributeName, attributeObject in mesh.geometry.attributes.items():
                attributeObject.uploadData()

            glDrawArrays( mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount )
            
            #mesh.material.updateRenderSettings() 

