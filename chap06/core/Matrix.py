import numpy
from numpy.typing import NDArray
from math import sin, cos, tan, pi

class Matrix:
    @staticmethod
    def makeIdentity():
        return numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def makeTranslation(x, y, z):
        return numpy.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def makeRotationX(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1]
        ]).astype(float)
    
    @staticmethod
    def makeRotationY(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array([
            [ c, 0, s, 0],
            [ 0, 1, 0, 0],
            [-s, 0, c, 0],
            [ 0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def makeRotationZ(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def makeScale(size):
        s = size
        return numpy.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod
    def makePerspective(angleOfView=60, aspectRatio=1.0, near=0.1, far=1000.0):
        a = angleOfView * pi/180.0
        d = 1.0 / tan(a/2)
        r = aspectRatio
        b = (far + near) / (near - far)
        c = 2*far*near / (near - far)
        return numpy.array([
            [d/r, 0,  0, 0],
            [0,   d,  0, 0],
            [0,   0,  b, c],
            [0,   0, -1, 0]
        ]).astype(float)
        
    @staticmethod
    def makeOrthographic(left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        a = 2 / ( right - left )
        b = 2 / ( top - bottom )
        c = -2 / ( far - near )

        l = -1 * ( ( right + left ) / ( right - left ) )
        m = -1 * ( ( top + bottom ) / ( top - bottom ) )
        n = -1 * ( ( far + near ) / ( far - near ) )

        return numpy.array([
            [a, 0, 0, l],
            [0, b, 0, m],
            [0, 0, c, n],
            [0, 0, 0, 1],
            ])
    
    @staticmethod
    def makeLookAt( objectPosition, targetPosition ):
        worldUp = [0, 1, 0]
        forward = numpy.subtract(targetPosition, objectPosition)

        right = numpy.cross(forward, worldUp)

        if ( numpy.linalg.norm( right ) < 0.001): 
            increment = numpy.array([0.001, 0, 0])
            right = numpy.cross(forward, worldUp + increment)

        up = numpy.cross(right, forward)

        # print(right, targetPosition)

        forward = numpy.divide( forward, numpy.linalg.norm(forward) )
        right = numpy.divide( right, numpy.linalg.norm(right) )
        up = numpy.divide( up, numpy.linalg.norm(up) )

        # print("UP: {}\nRIGHT: {}\nFORWARD: {}".format(up, right, forward))

        return numpy.array([
            [-right[0], up[0], forward[0], objectPosition[0]],
            [-right[1], up[1], forward[1], objectPosition[1]],
            [-right[2], up[2], forward[2], objectPosition[2]],
            [0, 0, 0, 1],
            ])

