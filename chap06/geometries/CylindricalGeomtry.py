from math import cos, pi, sin

from core.Matrix import Matrix

from geometries.ParametricGeometry import ParametricGeometry, PolygonGeometry


class CylindricalGeometry(ParametricGeometry):
    def __init__(self, radiusTop=1, radiusBottom=1, 
    height=1, radialSegments=32, heightSegments=4, 
    closedTop=True, closedBottom=True):
        def S(u, v):
            return[
                (v*radiusTop + (1-v)*radiusBottom)*
                sin(u), height * (v-0.5), 
                (v*radiusTop + (1-v)*radiusBottom)
                *cos(u)]
        super().__init__(0, 2*pi, radialSegments,
        0, 1, heightSegments, S)
        if closedTop:
            topGeometry = PolygonGeometry(
                radialSegments, radiusTop
            )
            transform = Matrix.makeTranslation(0, height*0.5, 0) @ Matrix.makeRotationY(-pi*0.5) @ Matrix.makeRotationX(-pi*0.5)

            topGeometry.applyMatrix(transform)
            self.merge(topGeometry)
        
        if closedBottom:
            bottomGeometry = PolygonGeometry(
                radialSegments, radiusBottom)
            transform = Matrix.makeTranslation(0, -height*0.5, 0) @ Matrix.makeRotationY(-pi*0.5) @ Matrix.makeRotationX(pi*0.5)
            bottomGeometry.applyMatrix(transform)
            self.merge(bottomGeometry)
