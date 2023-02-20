from materials.LightenedMaterial import LightenedMaterial
import OpenGL.GL as GL

"""
My understanding of how shading works in OpenGL:
    A grayscale depth texture is created first, generated with a virtual camera, with the same direction as that of the light
    and the same position; each fragment of that texture represents the distance of the object to the light source or virtual camera, so
    that darker fragments represent points that are closer, and brighter fragments points that are farther;

    Then in the fragment shader, the distance of the vector to the light source is calculated and then compared to the depth texture provided:
    if the value is lower (i.e. the vector has something covering its right line to the light source), then shade effects are applied over it, then shade effects are applied over it
    

    - - - - 

    ChatGPT said my reasoning is generally correct, but worth noticing that it's not the most adequate way of producing lights due to some limitations of the 
    mthod (it said is called shadow mapping): transparent or glass surfaces, for example, would cause shadows to be cast like any other material. 

    Me: You said it is 'generally correct'. Why? Is there anything wrong in my reasoning?

    GPT:There is nothing fundamentally incorrect with your description, but there are a few points that could be clarified or expanded upon.
    First, it's worth noting that the process you described is commonly known as shadow mapping, which is just one of many techniques for generating shadows in computer graphics.
    Second, while it's true that a depth texture is often used to store the distance of each fragment to the light source, it's not necessarily true that the texture is grayscale. In fact, it's often stored as a single component (the depth value) in a texture with a specific format, such as GL_DEPTH_COMPONENT.
    Third, the comparison between the depth texture and the distance to the light source is not done explicitly in the fragment shader. Rather, the depth texture is used to determine whether a given fragment is in shadow by performing a depth test during the rasterization stage of the rendering pipeline. If the depth of the fragment is greater than the depth stored in the depth texture at the same location, it is in shadow and the corresponding fragment shader code can be skipped entirely.
    Finally, the shadow mapping process can be more complex than what you described, involving techniques such as cascaded shadow maps, percentage closer filtering, or variance shadow maps, to name a few. The specific details of the technique can depend on the particular use case, hardware, and desired visual quality.
"""


class PhongMaterial(LightenedMaterial):

    def __init__(self,
                 texture = None,
                 properties = {},
                 numberOfLights = 1,
                 useShadow = False):

        super().__init__(numberOfLights=numberOfLights)

        if texture is None:
            self.addUniform("bool", "useTexture", False)
        else:
            self.addUniform("bool", "useTexture", True)
            self.addUniform("sampler2D", "texture", [texture.textureReference, 1])

        self.addUniform("vec3", "viewPosition", [0,0,0])
        self.addUniform("float", "specularStrength", 1.0)
        self.addUniform("float", "shininess", 32.0)

        if not useShadow:
            self.addUniform("bool", "useShadow", False)
        else:
            self.addUniform("bool", "useShadow", True)
            self.addUniform("Shadow", "shadow0", None)

        self.locateUniforms()

        self.settings["doubleSide"] = True
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1
        self.setProperties(properties)

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

        struct Shadow{
            vec3 lightDirection;
            mat4 projectionMatrix;
            mat4 viewMatrix;
            sampler2D depthTexture;
            float strength;
            float bias;
        };

        uniform bool useShadow;
        uniform Shadow shadow0;
        out vec3 shadowPosition0;

        void main(){
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV;
            position = vec3(modelMatrix * vec4(vertexPosition, 1.0));
            normal = normalize(mat3(modelMatrix) * vertexNormal);
            
            if ( useShadow ){
                vec4 temp0 = shadow0.projectionMatrix * shadow0.viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                shadowPosition0 = vec3(temp0);
            }

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

        uniform vec3 viewPosition;
        uniform float specularStrength;
        uniform float shininess;

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

                if (diffuse > 0) {
                    vec3 viewDirection = normalize(viewPosition - pointPosition);
                    vec3 reflectDirection = reflect(lightDirection, pointNormal);
                    specular = max( dot(viewDirection, reflectDirection), 0.0 );
                    specular = specularStrength * pow(specular, shininess);
                }
            }
            return light.color * (ambient + diffuse + specular);
        }

        uniform vec3 baseColor;
        uniform bool useTexture;
        uniform sampler2D texture;
        in vec3 position;
        in vec3 normal;
        in vec2 UV;
        out vec4 fragColor;

        struct Shadow{
            vec3 lightDirection;
            mat4 projectionMatrix;
            mat4 viewMatrix;
            sampler2D depthTexture;
            float strength;
            float bias;
        };

        uniform bool useShadow;
        uniform Shadow shadow0;
        uniform vec3 shadowPosition0;

        void main(){
            vec4 color = vec4(baseColor, 1.0);
            if (useTexture)
                color *= texture2D(texture, UV);

            vec3 total = vec3(0, 0, 0);

            """ + self.generateGLSLLightCalculations(destName="total") + """

            color *= vec4(total, 1);
            
            if (useShadow){
                // normalize to [0, 1] range, to be used as UV coordinates
                vec3 shadowCoord = ( shadowPosition0.xyz + 1.0 ) / 2.0;
                
                float closestDistanceToLight = texture2D(shadow0.depthTexture, shadowCoord.xy).r;
                float fragmentDistanceToLight = clamp(shadowCoord.z, 0, 1);

                bool isInShadow = fragmentDistanceToLight > ( closestDistanceToLight + shadow0.bias);

                float cosAngle = dot(normalize(normal), -normalize(shadow0.lightDirection));
                bool isFacingLight = (cosAngle > 0.01);

                if ( isFacingLight && isInShadow ) {
                    float s = 1.0 - shadow0.strength;
                    color *= vec4(s, s, s, 1);
                }

            }

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
