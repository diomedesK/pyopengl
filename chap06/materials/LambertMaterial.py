from materials.LightenedMaterial import LightenedMaterial
import OpenGL.GL as GL

class LambertMaterial(LightenedMaterial):
    """docstring for FlatMaterial"""

    def __init__(self, texture = None, bumpTexture = None, properties = {}, numberOfLights = 1):
        super().__init__(numberOfLights=numberOfLights)

        if texture is None:
            self.addUniform("bool", "useTexture", False)
        else:
            self.addUniform("bool", "useTexture", True)
            self.addUniform("sampler2D", "texture", [texture.textureReference, 1])

        if bumpTexture is None:
            self.addUniform("bool", "useBumpTexture", False)
        else:
            self.addUniform("bool", "useBumpTexture", True)
            self.addUniform("sampler2D", "bumpTexture", [ bumpTexture.textureReference, 2 ])
            self.addUniform("float", "bumpStrength", 1.0)


        self.locateUniforms()

        self.settings["doubleSide"] = True
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1
        self.setProperties(self.settings)

    @property
    def vertexShaderCode(self):
        code = """
        uniform mat4 modelMatrix;
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        in vec3 vertexPosition;
        in vec3 vertexNormal;
        in vec2 vertexUV;
        out vec2 UV;
        out vec3 position;
        out vec3 normal;

        void main(){
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV;
            position = vec3(modelMatrix * vec4(vertexPosition, 1.0));
            normal = normalize(mat3(modelMatrix) * vertexNormal);
        }
        """

        return code
    
    @property
    def fragmentShaderCode(self):
        code = """
        struct Light{
            int lightType; // defaults as ambient
            vec3 color;
            vec3 position;
            vec3 direction;
            vec3 attenuation;
        };
        """ + self.generateGLSLLightUniforms() + """

        vec3 calculateLight(Light light, vec3 pointPosition, vec3 pointNormal)
        {
            float ambient = 0;
            float diffuse = 0;
            float specular = 0;
            float attenuation = 1;
            vec3 lightDirection = vec3(0, 0, 0);
            
            if (light.lightType == 1)  // ambient light
            {
                ambient = 1;
            }
            else if (light.lightType == 2)  // directional light 
            {
                lightDirection = normalize(light.direction);
            }
            else if (light.lightType == 3)  // point light 
            {
                lightDirection = normalize(pointPosition - light.position);
                float distance = length(light.position - pointPosition);
                attenuation = 1.0 / (light.attenuation[0] 
                                   + light.attenuation[1] * distance 
                                   + light.attenuation[2] * distance * distance);
            }
            
            if (light.lightType > 1)  // directional or point light
            {
                pointNormal = normalize(pointNormal);
                diffuse = max(dot(pointNormal, -lightDirection), 0.0);
                diffuse *= attenuation;
            }
            return light.color * (ambient + diffuse + specular);
        }

        uniform vec3 baseColor;
        uniform bool useTexture;
        uniform sampler2D texture;

        uniform bool useBumpTexture;
        uniform sampler2D bumpTexture;
        uniform float bumpStrength;

        in vec3 position;
        in vec3 normal;
        in vec2 UV;
        out vec4 fragColor;

        void main(){
            vec4 color = vec4(baseColor, 1.0);
            if (useTexture)
                color *= texture2D(texture, UV);

            vec3 total = vec3(0, 0, 0);

            if (useBumpTexture)
                total += bumpStrength * vec3(texture2D(bumpTexture, UV));

            """ + self.generateGLSLLightCalculations(destName="total") + """

            color *= vec4(total, 1);
            fragColor = color;
        }
        """

        return code

    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        if self.settings["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(self.settings["lineWidth"])
