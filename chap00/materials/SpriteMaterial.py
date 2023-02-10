from core.Material import Material

from OpenGL.GL import *

class SpriteMaterial(Material):
    """docstring for SpriteMaterial"""
    def __init__(self, texture, properties={}):
        vertexShaderCode = """
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform mat4 projectionMatrix;
        uniform bool billboard;

        uniform float tileNumber;
        uniform vec2 tileCount;

        in vec3 vertexPosition;
        in vec2 vertexUV; 

        out vec2 UV;

        void main(){
            mat4 _tmpM4 = viewMatrix * modelMatrix;

            if (billboard){
                _tmpM4[0][0] = 1;
                _tmpM4[0][1] = 0;
                _tmpM4[0][2] = 0;
                _tmpM4[1][0] = 0;
                _tmpM4[1][1] = 1;
                _tmpM4[1][2] = 0;
                _tmpM4[2][0] = 0;
                _tmpM4[2][1] = 0;
                _tmpM4[2][2] = 1;
            }

            gl_Position = projectionMatrix * _tmpM4 * vec4(vertexPosition, 1.0);
            
            if ( tileNumber > 1.0 ) {
                vec2 tileSize = 1.0 / tileCount;
                UV = vertexUV;

                float columnIndex = mod(tileNumber, tileCount[0]);
                float rowIndex = floor(tileNumber / tileCount[0]);

                vec2 tileOffset = vec2( 
                    columnIndex / tileCount[0],
                    1.0 -  (rowIndex + 1.0) / tileCount[1]
                    );

                UV = UV * tileSize + tileOffset;
            }
        }
        """

        fragmentShaderCode = """
            in vec2 UV;
            uniform vec3 baseColor;
            uniform sampler2D texture;

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

        self.addUniform("bool", "billboard", False)
        self.addUniform("float", "tileNumber", -1.0)
        self.addUniform("vec2", "tileCount", [1, 1])
        self.addUniform("sampler2D", "texture", [texture.textureReference, 1])
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])

        self.locateUniforms()

        self.settings["doubleSide"] = True
        self.setProperties(properties)

    def updateRenderSettings(self):

        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        
