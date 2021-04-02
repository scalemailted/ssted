from .EntityEvent import EntityEvent
#from itertools import islice
from ..ent.Point import Point

class ContinuousEntityEvent: #(EntityEvent):
    def __init__(self, uid, startingTime, startingValue, model):
        self.uid = uid
        self.startTime = startingTime
        self.startValue = startingValue
        self.model = model

    def getStartTime(self):
        return self.startTime

    def getUID(self):
        return self.uid

    def getIter(self):
        return self.iterator(self.startValue, self.model)

    class iterator:
        def __init__(self, startValue, model):
            self.current = startValue
            self.model = model
            #print('ContinuityEvent iterator --> current type',type(self.current))
            #if isinstance(self.current, Point):
            #    print('ContinuityEvent iterator constructor',self.current, id(self.current))
        def __next__(self):
            #if isinstance(self.current, Point):
            #    print('ContinuityEvent iterator next [before]',self.current, id(self.current))
            #self.current = self.model(self.current)
            self.model(self.current)
            #if isinstance(self.current, Point):
            #    print('ContinuityEvent iterator next [after]',self.current, id(self.current))
            return self.current


"""
class ContinuousEntityEvent(EntityEvent):
    def __init__(self, uid, startingTime, startingValue, model):
        self.time = startingTime
        self.model = model[startingTime:]
        self.uid = uid
        self.startingValue = startingValue

    def getStartTime(self):
        return self.time

    def getUID(self):
        return self.uid

    def consume(self, iterator, n):
        next(islice(iterator, n, n), None)

    def getIter(self):
        it = iter(self.model)
        self.consume(it, 1)
        return  it
"""

"""
package timeseries

import scala.collection.Iterator
import ent.Entity

class ContinuousEntityEvent[T <: Entity[T]](uid: Int, startingTime: Int, startingValue: T)(model: (T) => T) extends EntityEvent {
    val time = startingTime
    val this.model = model

    def getStartTime = time
    def getUID = uid
    def getIter = Iterator.iterate[T](startingValue)(model).drop(1)
}
"""

"""
class foo:
    def __init__(self,start,model):
        self.start = start 
        self.model = model
        self.current = start
    def __next__(self):
        self.current = self.model(self.current)
        return self.current

"""



