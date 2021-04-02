from ..ent.Weight import Weight
from abc import ABC, abstractmethod

class Weighted(ABC):
    @abstractmethod
    def getWeight(self):
        """Must implement method to return weight"""


"""
package graph

import ent.Weight

trait Weighted {
  def getWeight: Weight
}
"""
