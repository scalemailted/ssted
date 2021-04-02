from ..ent.Weight import Weight
from .Weighted import Weighted

#Specifies a temporal edge where source and destination are immutable.
class TEdge(Weighted):
    def __init__(self, uniqueId, source, destination, initialWeight=None):
        self.uid = uniqueId
        self.src = source
        self.dst = destination
        self.weight = initialWeight

    def getWeight(self):
        return self.weight

    def __eq__(self, other):
        if isinstance(other,TEdge) and self.uid == other.uid:
            return True
        return False

    def __hash__(self):
        return hash(self.uid);

    def __str__(self): 
        return f"{self.uid};({self.src},{self.dst});[{self.weight}];"


"""
package graph

import ent.Weight

/**
  * Specifies a temporal edge where source and destination are immutable.
  */
class TEdge(uniqueId: String, source: String, destination: String, initialWeight: Weight = null) extends Weighted {
  val uid = uniqueId
  val src = source
  val dst = destination
  val weight = initialWeight

  def getWeight = weight

  override def equals(arg: Any): Boolean = {
    arg match {
      case arg: TEdge => uid == arg.uid
      case _          => false
    }
  }

  override def hashCode() = uid.hashCode();

  override def toString() = s"$uid;($src,$dst);[$weight];"
}
"""