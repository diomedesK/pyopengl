from core.Matrix import Matrix
from core.Mesh import Mesh
from OpenGL.GL import *

import numpy, pygame

debug = True

class Renderer(object):
    """docstring for Renderer"""
    def __init__(self):
        super(Renderer, self).__init__()
        glEnable(GL_DEPTH_TEST)
        #require for antialiasing
        glEnable(GL_MULTISAMPLE)
        glClearColor(0, 0, 0, 1)
        #support transparent textures
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.windowSize = pygame.display.get_surface().get_size()
        self.meshFilter = lambda x : isinstance(x, Mesh)


    def render(self, scene, camera, meshHandler = None, clearColor = True, clearDepth = True, renderTarget = None):
        if renderTarget == None:
            # 0 is the default reference to the default window-system-provided framebuffer
            glBindFramebuffer(GL_FRAMEBUFFER, 0) 
            glViewport(0, 0, self.windowSize[0], self.windowSize[1])
        else:
            glBindFramebuffer(GL_FRAMEBUFFER, renderTarget.framebufferRef) 
            glViewport(0, 0, renderTarget.width, renderTarget.height)

        if clearColor:
            glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth:
            glClear(GL_DEPTH_BUFFER_BIT)

        camera.updateViewMatrix()

        meshList = list(filter(self.meshFilter, scene.getDescendantsList()))

        for mesh in meshList:

            if meshHandler is not None:
                meshHandler(mesh)

            glUseProgram(mesh.material.program)

            glBindVertexArray(mesh.VAO)
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["modelMatrix"].data = mesh.transform
            
            for uniformName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
                pass

            mesh.material.updateRenderSettings()

            glDrawArrays( mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount )
            
