from ..ent.Entity import Entity
from .EntityEvent import EntityEvent

class SingleEntityEvent(EntityEvent):
    def __init__(self, uid, time, value, model):
        self.uid = uid
        self.time = time
        self.value = value
        self.model = model
    
    def getStartTime(self):
        return self.time
    
    def getUID(self):
        return self.uid
    
    def getIter(self):
        return self.iterator(1, self.value, self.model)

    class iterator:
        def __init__(self, count, value, model):
            self.count = count
            self.current = value
            self.model = model
        def __next__(self):
            if self.count > 0:
                self.count -= 1
                #self.current = self.model(self.current)
                #return self.current
                return self.model(self.current)
            else:
                return None

"""
package timeseries

import scala.collection.Iterator
import ent.Entity

class SingleEntityEvent[T <: Entity[T]](uid: Int, time: Int, value: T)(model: (T) => T) extends EntityEvent {
  val this.time = time
  val this.model = model

  def getStartTime = this.time
  def getIter = Iterator.fill[T](1)(model(value)) //Fill takes elt computation (lazy eval)
  def getUID = uid
}
"""
