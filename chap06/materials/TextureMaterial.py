from core.Material import Material
from OpenGL.GL import *

class TextureMaterial(Material):
    """Create a texture surface"""
    def __init__(self, texture, properties={}):

        vertexShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        in vec3 vertexPosition;
        in vec2 vertexUV;
        
        uniform vec2 repeatUV;
        uniform vec2 offsetUV;
        out vec2 UV;

        void main(){
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV * repeatUV + offsetUV;
        }

        """
        fragmentShaderCode = """
        uniform vec3 baseColor;
        uniform sampler2D texture; /* stores a texture unit */
        in vec2 UV;
        out vec4 fragColor;

        void main(){
            vec4 color = vec4(baseColor, 1.0) * texture2D(texture, UV);

            if ( color.a < 0.10 ){
                discard;
            }
            fragColor = color;
        }
        """
        super().__init__(vertexShaderCode, fragmentShaderCode)

        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0, 1.0])
        self.addUniform("sampler2D", "texture", [texture.textureReference, 1])
        self.addUniform("vec2", "repeatUV", [+1.0, +1.0])
        self.addUniform("vec2", "offsetUV", [+1.0, +1.0])

        self.locateUniforms()

        self.settings["doubleSide"] = True
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1

        self.setProperties(properties)
    
    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        
        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glLineWidth(self.settings["lineWidth"])

