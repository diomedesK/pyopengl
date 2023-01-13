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
        super().__init__(frameRate=10)

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
        uniform float timer;
        
        /* these numbers are just random values which occur to form a nice texture*/
        float random(vec2 UV_values){
            return fract(235711.0 * sin(14.337*UV_values.x + 42.418*UV_values.y) );
        }

        float boxRandom(vec2 UV_values, float scale){
            vec2 iScaleUV = floor(UV_values * scale * (timer/timer));
            return random(iScaleUV);
        }

        float smoothRandom(vec2 UV_values, float scale){
            vec2 iScaleUV = floor(scale * UV_values);
            vec2 fScaleUV = fract(scale * UV_values);
            float a = random(iScaleUV); // + vec2(0, 0)
            float b = random(round(iScaleUV + vec2(1, 0)));
            float c = random(round(iScaleUV + vec2(0, 1)));
            float d = random(round(iScaleUV + vec2(1, 1)));
            return mix(
                mix(a, b, fScaleUV.x),
                mix(c, d, fScaleUV.x),
                fScaleUV.y
                );
        }

        // add smooth random values at different scales
        // weighted (amplitudes) so that sum is approximately 1.0

        float fractalRandom(vec2 UV_value, float scale) {
            float value = 0.0;
            float amplitude = 0.5;
            for (int i = 0; i < 6; i++)
            {
            value += amplitude * smoothRandom(UV_value, scale);
            scale *= 2.0;
            amplitude *= 0.5;
            }
            return value;
        }

        void main(){
            /*
            vec4 color1 = vec4(1.0, 0.0, 0.0, 1);
            vec4 color2 = vec4(0.0, 0.0, 1.0, 1);
            fragColor = mix( color1, color2, 0.5 );
            */
            
            float r1 = boxRandom(UV, 10.0);
            float r2 = smoothRandom(UV, 10.0);

            // fragColor = mix( vec4(r1, r1, r1, 1.0), vec4(r2, r2, r2, 1.0), abs( sin(timer) ));
            fragColor = vec4(r1, r1, r1, 1.0);

        }
        """

        self.geo = RectangleGeometry()
        self.mat = Material(vertex_sh, fragme_sh)
        
        self.mat.addUniform("float", "timer", 0.0)
        self.mat.locateUniforms()

        self.mesh = Mesh(self.geo, self.mat)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.mat.uniforms["timer"].data += self.deltaTime * 1/16;
        # print("{:.2f}".format( self.timer ))

Graphics().run()
