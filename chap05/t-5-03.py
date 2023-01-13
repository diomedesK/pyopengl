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
        self.scene = Scene()
        self.renderer = Renderer()
        self.camera = Camera()

        vertex_sh = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        in vec3 vertexPosition;
        in vec2 vertexUV;
        
        out vec2 UV;

        void main(){
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);

            UV = vertexUV;
        }
        """

        fragme_sh = """
        uniform sampler2D texture;
        uniform float time;

        in vec2 UV;

        out vec4 fragColor;
        
        void main(){
            vec2 shiftUV = UV + vec2(0, 0.5 * sin(6.0*UV.x + time));
            fragColor = texture2D(texture, shiftUV);
        }
        """

        myTexture = Texture("./images/grid.png")

        self.geo = RectangleGeometry()
        self.mat = Material(vertex_sh, fragme_sh)

        self.mat.addUniform("sampler2D", "texture", [myTexture.textureReference, 1])
        self.mat.addUniform("float", "time", 0.0)

        self.mat.locateUniforms()

        self.camera.setPosition([0, 0, 4])
        
        self.mesh = Mesh(self.geo, self.mat)
        self.scene.add(self.mesh)

        glDisable(GL_CULL_FACE)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.mat.uniforms["time"].data += self.deltaTime

        # self.mesh.rotateX(1 * abs( math.sin(self.deltaTime) ))
        # self.mesh.rotateY(1 * abs( math.sin(self.deltaTime) ))
        # self.mesh.rotateZ(1 * abs( math.sin(self.deltaTime) ))
        
Graphics().run()
