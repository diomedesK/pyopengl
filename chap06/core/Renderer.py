from core.Matrix import Matrix
from core.Mesh import Mesh
from light.Light import Light
from OpenGL.GL import *

import numpy, pygame

debug = True

class Renderer(object):
    """docstring for Renderer"""
    def __init__(self, clearColor = [0, 0, 0, 1]):
        super(Renderer, self).__init__()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE) #required for antialiasing

        glClearColor(*clearColor)

        self.windowSize = pygame.display.get_surface().get_size()
        self.meshFilter = lambda x : isinstance(x, Mesh)
        self.lightFilter = lambda x : isinstance(x, Light)

    def render(self, scene, camera, meshHandler = None, clearColor = True, clearDepth = True, renderTarget = None):
        if renderTarget == None:
            # 0 is the default reference to the default window-system-provided framebuffer
            glBindFramebuffer(GL_FRAMEBUFFER, 0) 
            glViewport(0, 0, *self.windowSize)
        else:
            glBindFramebuffer(GL_FRAMEBUFFER, renderTarget.framebufferRef) 
            glViewport(0, 0, renderTarget.width, renderTarget.height)

        if clearColor:
            glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth:
            glClear(GL_DEPTH_BUFFER_BIT)

        glEnable(GL_BLEND) #support transparent textures
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        camera.updateViewMatrix()

        sceneDescendantsList = scene.getDescendantsList()
        meshList = list(filter(self.meshFilter, sceneDescendantsList))
        lightList = list(filter(self.lightFilter, sceneDescendantsList))

        for mesh in meshList:

            if not mesh.visible:
                continue

            meshHandler(mesh) if meshHandler else None

            glUseProgram(mesh.material.program)
            glBindVertexArray(mesh.VAO)

            mesh.material.uniforms["modelMatrix"].data = mesh.getWorldTransform()
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix

            if "light0" in mesh.material.uniforms.keys():
                for lightNumber, lightInstance in enumerate(lightList):
                    mesh.material.uniforms[f"light{lightNumber}"].data = lightInstance

            if "viewPosition" in mesh.material.uniforms.keys():
                mesh.material.uniforms["viewPosition"].data = camera.getWorldPosition()
            
            for uniformName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
                pass

            mesh.material.updateRenderSettings()
            glDrawArrays( mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount )
            
