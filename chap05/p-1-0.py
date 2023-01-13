from core.Base import Base
from core.Material import Material
from core.Scene import Scene
from core.Mesh import Mesh
from core.Renderer import Renderer
from core.Camera import Camera
from core.Texture import Texture

from geometries.RectangleGeometry import RectangleGeometry

import math
from OpenGL.GL import *

class Graphics(Base):
    def __init__(self):
        super().__init__()

    def initialize(self):
        glDisable(GL_CULL_FACE)

        self.scene = Scene()
        self.renderer = Renderer()
        self.camera = Camera()

        self.camera.setPosition([0, 0, 2])

        vertex_sh = """
        uniform mat4 projectionMatrix;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        
        in vec3 vertexPosition;
        in vec2 vertexUV;

        out vec2 UV;

        void main(){
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);

            UV = vertexUV;
        }
        """

        fragme_sh = """
        in vec2 UV;
        out vec4 fragColor;
        
        float random(vec2 UV_values){
            return fract(235711.0 * sin(14.337*UV_values.x + 42.418*UV_values.y));
        }

        void main(){
            float r  = random(UV);
            fragColor = vec4(r, r, r, 1);
        }
        """

        self.geo = RectangleGeometry()
        self.mat = Material(vertex_sh, fragme_sh)

        self.mat.locateUniforms()

        
        self.mesh = Mesh(self.geo, self.mat)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)

Graphics().run()
