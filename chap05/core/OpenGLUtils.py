from OpenGL.GL import *

class OpenGLUtils(object):

    @staticmethod
    def __compileShader(code, kind):
        code = '#version 330 \n' + code

        shader = glCreateShader(kind)
        glShaderSource(shader, code)
        glCompileShader(shader)
        compileSuccess = glGetShaderiv( shader, GL_COMPILE_STATUS)
        if not compileSuccess:
            compilingLog = '\n' + glGetShaderInfoLog(shader).decode('utf-8')
            glDeleteShader(shader)

            raise Exception(compilingLog)
        else:
            print(f"{kind} compiled successfully")

        return shader

    @staticmethod
    def initializeProgram(vertexShaderCode, fragmentShaderCode):
        vertex_shader_ref = OpenGLUtils.__compileShader(vertexShaderCode, GL_VERTEX_SHADER)
        fragment_shader_ref = OpenGLUtils.__compileShader(fragmentShaderCode, GL_FRAGMENT_SHADER)
        
        program = glCreateProgram();
        glAttachShader(program, vertex_shader_ref)
        glAttachShader(program, fragment_shader_ref)

        glLinkProgram(program)

        linkSuccess = glGetProgramiv(program, GL_LINK_STATUS)
        if not linkSuccess:
            linkingLog = "\n" + glGetProgramInfoLog(program)
            glDeleteProgram(program)
            raise Exception(linkingLog)

        return program



    @staticmethod
    def printSystemInfo():
        print(" Vendor: " + glGetString(GL_VENDOR).decode('utf-8'))
        print("Renderer: " + glGetString(GL_RENDERER).decode('utf-8'))
        print("OpenGL version supported: " + glGetString(GL_VERSION).decode('utf-8'))
        print("GLSL version supported: " + glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8'))
