from .GlobalEvent import GlobalEvent

class ContinuousGlobalEvent: #(GlobalEvent):
    def __init__(self, uid, startingTime, world, model):
        self.uid = uid
        self.startTime = startingTime
        self.world = world
        self.model = model

    def getStartTime(self):
        return self.startingTime

    def getUID(self):
        return self.uid

    def getIter(self):
        return self.iterator(self.world, self.model)
        
    class iterator:
        def __init__(self, world, model):
            self.current = world
            self.model = model
        def __next__(self):
            self.current = self.model(self.current)
            return self.current


"""
package timeseries

class ContinuousGlobalEvent[T](uid: Int, startingTime: Int, world: T)(model: (T) => T) extends GlobalEvent {
  val time = startingTime
  val this.model = model

  def getStartTime = time
  def getUID = uid
  def getIter = Iterator.iterate[T](world)(model).drop(1)
}
"""
