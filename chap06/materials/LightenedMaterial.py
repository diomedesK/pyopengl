from core.Material import Material

class LightenedMaterial(Material):
    """docstring for LightenedMaterial"""
    def __init__(self, numberOfLights = 4):
        self.numberOfLights = numberOfLights
        super(LightenedMaterial, self).__init__(self.vertexShaderCode, self.fragmentShaderCode)

        for n in range(self.numberOfLights):
            self.addUniform("Light", "light"+str(n), None)

    @property
    def vertexShaderCode(self):
        raise NotImplementedError("Please, implement this property for an inherited class")

    @property
    def fragmentShaderCode(self):
        raise NotImplementedError("Please, implement this property for an inherited class")

    def generateGLSLLightUniforms(self):
        return "\n" + "\n".join(f"\t\t\tuniform Light light{i};" for i in range(self.numberOfLights)) + "\n"

    def generateGLSLLightCalculations(self, destName = "light"):
        return "\n" + "\n".join(f"\t\t\t{destName} += calculateLight(light{i}, position, normal);"
                                for i in range(self.numberOfLights)) + "\n"
    
