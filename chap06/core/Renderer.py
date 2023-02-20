from core.Matrix import Matrix
from core.Mesh import Mesh
from light.Light import Light
from OpenGL.GL import *

from light.AmbientLight import AmbientLight
from light.Shadow import Shadow

import numpy, pygame

class Renderer(object):
    def __init__(self, clearColor = [0, 0, 0, 1]):
        super(Renderer, self).__init__()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE) #required for antialiasing

        glClearColor(*clearColor)

        self.windowSize = pygame.display.get_surface().get_size()
        self.meshFilter = lambda x : isinstance(x, Mesh)
        self.lightFilter = lambda x : isinstance(x, Light)

        self.shadowsEnabled = False

    def render(self, scene, camera, meshHandler = None, clearColor = True, clearDepth = True, renderTarget = None):

        sceneDescendantsList = scene.getDescendantsList()
        meshList = list(filter(self.meshFilter, sceneDescendantsList))
        lightList = list(filter(self.lightFilter, sceneDescendantsList))

        if self.shadowsEnabled:
            glBindFramebuffer(GL_FRAMEBUFFER, self.shadowObject.renderTarget.framebufferRef)
            glViewport(0, 0, self.shadowObject.renderTarget.width, self.shadowObject.renderTarget.height )
            glClearColor(1, 1, 1, 1)

            glClear(GL_COLOR_BUFFER_BIT)
            glClear(GL_DEPTH_BUFFER_BIT)

            glUseProgram(self.shadowObject.material.program)
            self.shadowObject.updateInternal()

            for mesh in meshList:
                if not mesh.visible:
                    continue

                if mesh.material.settings["drawStyle"] != GL_TRIANGLES:
                    continue

                glBindVertexArray(mesh.VAO)
                self.shadowObject.material.uniforms["modelMatrix"].data = mesh.getWorldTransform()

                for uniformName, uniformObject in self.shadowObject.material.uniforms.items():
                    uniformObject.uploadData()
                
                glDrawArrays( GL_TRIANGLES, 0, mesh.geometry.vertexCount )


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

                lightNumber = 0
                for lightInstance in lightList:
                    mesh.material.uniforms[f"light{lightNumber}"].data = lightInstance
                    lightNumber += 1

                while lightNumber < mesh.material.numberOfLights:
                    mesh.material.uniforms[f"light{lightNumber}"].data = AmbientLight([0.0 for n in range(3)])
                    lightNumber += 1

            if "viewPosition" in mesh.material.uniforms.keys():
                mesh.material.uniforms["viewPosition"].data = camera.getWorldPosition()

            if self.shadowsEnabled and "shadow0" in mesh.material.uniforms.keys():
                mesh.material.uniforms["shadow0"].data = self.shadowObject
            
            for uniformName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()

            mesh.material.updateRenderSettings()
            glDrawArrays( mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount )
        
    def enableShadows(self, lightSource, strength = 0.5, resolution = [512, 512]):
        self.shadowsEnabled = True
        self.shadowObject = Shadow(lightSource, strength=strength, resolution=resolution)
