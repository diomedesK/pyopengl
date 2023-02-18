from typing import Union
from math import cos, pi, sin

from geometries.EllipsoidGemetry import EllipsoidGeometry

class SphereGeometry(EllipsoidGeometry):
    def __init__(self, radius: Union[int, float], radiusSegments=32, heightSements=16):
        super().__init__(2*radius, 2*radius, 2*radius, radiusSegments, heightSements)
