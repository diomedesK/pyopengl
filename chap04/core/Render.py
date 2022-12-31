from core.Mesh import Mesh
from OpenGL.GL import *

# First the Render class will apply some settings to the OpenGL environment,
# then the class will iterate over each visible mesh in the scene graph and apply 
# the owing transformations over it, and finally it will handle the actual display on the screen.

class Renderer(object):
    """Effectively responsible for performing general rendering related tasks"""
    def __init__(self, clearColor = [0, 0, 0]):
        super().__init__()
        glEnable( GL_DEPTH_TEST )
        glEnable( GL_MULTISAMPLE )
        glClearColor( clearColor[0], clearColor[1], clearColor[2], 1) 

    def render(self, scene, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #pyright: ignore
        camera.updateViewMatrix()
        
        sceneDescendantsList = scene.getDescendantsList()
        meshList = list(filter(lambda a : isinstance(a, Mesh), sceneDescendantsList))

        for mesh in meshList:
            if not mesh.visible:
                continue

            glUseProgram(mesh.material.program)
            glBindVertexArray(mesh.VAO)

            mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix

            for index, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()

            mesh.material.updateRenderSettings()
            glDrawArrays(mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount)
