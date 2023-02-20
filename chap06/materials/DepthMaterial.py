from core.Material import Material

class DepthMaterial(Material):
    def __init__(self):

        vertexShaderCode = """
        in vec3 vertexPosition;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform mat4 projectionMatrix;

        void main(){
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }

        """

        fragmentShaderCode = """
        out vec4 fragColor;
        
        void main(){
            float depth = gl_FragCoord.z;
            fragColor = vec4(depth, depth, depth, 1);
        }
        """

        super().__init__(vertexShaderCode, fragmentShaderCode)
        self.locateUniforms()

    def updateRenderSettings(self):
        pass
