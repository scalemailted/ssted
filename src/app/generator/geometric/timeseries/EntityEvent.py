from ..ent.Entity import Entity
from .Event import Event
from abc import abstractmethod

class EntityEvent(Event): 
    @abstractmethod
    def getIter(self):
        """must implement method that returns iterator"""



"""
package timeseries

import scala.collection.Iterator
import ent.Entity

trait EntityEvent extends Event{
  override def getIter: Iterator[_ <: Entity[_]]
}
"""