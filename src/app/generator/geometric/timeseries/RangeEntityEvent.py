from ..ent.Entity import Entity
from .EntityEvent import EntityEvent

class RangeEntityEvent(EntityEvent):
    def __init__(self, uid, startTimeInclusive, endTimeExclusive, variable, model):
        self.uid = uid
        self.starttime = startTimeInclusive
        self.endtime = endTimeExclusive
        self.variable = variable
        self.model = model
    
    def getStartTime(self):
        return self.starttime
    
    def getUID(self):
        return self.uid
    
    def getIter(self):
        return self.iterator(self.endtime-self.starttime, self.variable, self.model)

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

//Note that this is almost an exact duplicate and may replace SingleEvent
class RangeEntityEvent[T <: Entity[T]](uid: Int, startTimeInclusive: Int, endTimeExclusive: Int, variable: T)(model: (T) => T)
  extends EntityEvent {
  val time = startTimeInclusive
  val this.model = model

  def getStartTime = startTimeInclusive
  def getIter = Iterator.fill[T](endTimeExclusive-startTimeInclusive)(model(variable)) //Lazy eval
  def getUID = uid
}
"""