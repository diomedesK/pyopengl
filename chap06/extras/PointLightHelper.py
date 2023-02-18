from core.Mesh import Mesh
from geometries.SphereGeometry import SphereGeometry
from materials.SurfaceMaterial import SurfaceMaterial

class PointLightHelper(Mesh):
    """docstring for PointLightHelper"""
    def __init__(self, pointLight, size=0.22, lineWidth=1):
        color = pointLight.color
        geometry = SphereGeometry(radius = size, radiusSegments=4, heightSements=2)
        material = SurfaceMaterial({
            "baseColor": color,
            "wireframe": True,
            "doubleSide": True,
            "lineWidth": lineWidth
        })

        super().__init__(geometry, material)
        
