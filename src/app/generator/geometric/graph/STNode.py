from ..ent.Point import Point
from .Spatial import Spatial

"""
  * Specifies a SpatioTemporal Node
"""
class STNode(Spatial):
    def __init__(self, uniqueId, initialPosition=None):
        self.uid = uniqueId
        self.position = initialPosition
        #print('stnode point', self.position, id(self.position))
        super().__init__()

    def getPos(self):
        return self.position

    def __eq__(self, other):
        if isinstance(other, STNode) and other.uid == self.uid:
            return True
        return False

    def __hash__(self):
        return hash(self.uid)

    def __str__(self):
        return f"{self.uid};[List{self.position}];"

