from .Entity import Entity

class Weight(Entity):
    def __init__(self, initialValue):
        self.mag = initialValue
        self.eventUIDSet = set()

    # overload + operator
    def __add__(self, other): 
        #return self.a + other.a, self.b + other.b 
        #print('weight +', other)
        if isinstance(other, Weight):
            sum = self.mag + other.mag
            self.mag = sum
            #return  Weight(sum)
        elif isinstance(other, (float,int)):
            sum = self.mag + other
            self.mag = sum
            #return Weight(sum)
    
    #overload == operator
    def __eq__(self, other):
        if isinstance(other, Weight) and self.mag == other.mag:
            return True
        return False

    #toString method
    def __str__(self):
        return  "Mag(" + str(self.mag) + ")"

    #add uid to event uid set
    def bindEvent(self, uid):
        self.eventUIDSet.add(uid)
    
    #remove uid from set
    def unbindEvent(self, uid):
        self.eventUIDSet.remove(uid)
    
    #get event uids
    def getBindings(self):
        return self.eventUIDSet



"""
import scala.collection.mutable

class Weight(initialValue: Double) extends Entity[Weight] {
    var mag: Double = initialValue
    val eventUIDSet = mutable.HashSet[Int]()

    def +(that: Weight) = { mag = mag + that.mag; this }
    def +(that: Double) = { mag = mag + that; this }
    def :=(that: Weight) = { mag = that.mag; this }
    def :=(that: Double) = { mag = that; this }

    override def toString() = "Mag(" + mag.toString + ")"

    def bindEvent(uid: Int) = eventUIDSet += uid
    def unbindEvent(uid: Int) = eventUIDSet -= uid
    def getBindings = eventUIDSet.toSet
}
"""
