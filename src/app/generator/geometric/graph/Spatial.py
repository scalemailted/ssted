from ..ent.Point import Point
from abc import ABC, abstractmethod

class Spatial(ABC):
    @abstractmethod
    def getPos(self):
        """Must implement method to return position"""