from ..ent.Entity import Entity
from .EntityEvent import EntityEvent

class PathEntityEvent(EntityEvent):
    def __init__(self, uid, startingTime, variable, path, model):
        self.uid = uid
        self.time = startingTime
        self.value = variable
        self.path = path
        self.model = model
    
    def getStartTime(self):
        return self.time
    
    def getUID(self):
        return self.uid
    
    def getIter(self):
            return self.iterator(len(self.path), self.value, iter(self.path) ,self.model)

    class iterator:
        def __init__(self, count, variable, seqIter, model):
            self.count = count
            self.variable = variable
            self.seqIter = seqIter
            self.model = model
        def __next__(self):
            if self.count > 0:
                self.count -= 1
                nextIter = next(self.seqIter, None)
                if nextIter:
                    return self.model(self.variable, nextIter)
            return None


"""
class PathEntityEvent(EntityEvent):
    def __init__(self, uid, startingTime, variable, path, model):
        self.uid = uid
        self.time = startingTime
        self.value = variable
        self.path = path
        self.seqIter = iter(path)
        self.model = model
    
    def getStartTime(self):
        return self.time
    
    def getUID(self):
        return self.uid
    
    def getIter(self):
            return self.iterator(len(self.path), self.value, self.seqIter ,self.model)

    class iterator:
        def __init__(self, count, variable, seqIter, model):
            self.count = count
            #self.current = value
            self.variable = variable
            self.seqIter = seqIter
            self.model = model
        def __next__(self):
            if self.count > 0:
                self.count -= 1
                nextIter = next(self.seqIter, None)
                if nextIter:
                    return self.model(self.variable, nextIter)
            return None
"""

"""
class PathEntityEvent(EntityEvent):
    def __init__(self, uid, startingTime, variable, path, model):
        self.uid = uid
        self.time = startingTime
        self.value = variable
        self.path = path
        self.seqIter = iter(path)
        self.model = model
    
    def getStartTime(self):
        return self.time
    
    def getUID(self):
        return self.uid
    
    def getIter(self):
        nextIter = next(self.seqIter, None)
        if nextIter:
            return self.iterator(len(self.path), self.value, nextIter ,self.model)
        else:
            return None

    class iterator:
        def __init__(self, count, variable, nextIter, model):
            self.count = count
            #self.current = value
            self.variable = variable
            self.nextIter = nextIter
            self.model = model
        def __next__(self):
            if self.count > 0:
                self.count -= 1
                return self.model(self.variable, self.nextIter)
            else:
                return None
"""

"""
package timeseries

import scala.collection.Iterator
import ent.Entity

class PathEntityEvent[T <: Entity[T]](uid: Int, startingTime: Int, variable: T, path: Seq[T])(model: (T,T) => T)
 extends EntityEvent {
  val time = startingTime
  val seqIter = path.toIterator
  val this.model = model

  def getStartTime = this.time
  def getIter = if ( seqIter.hasNext ) Iterator.fill[T](path.size)(model(variable, seqIter.next()))
                else Iterator.empty
  def getUID = uid
}
"""