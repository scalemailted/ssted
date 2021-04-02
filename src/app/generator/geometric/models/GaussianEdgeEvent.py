from ..timeseries.ContinuousEntityEvent import ContinuousEntityEvent
from ..timeseries.SingleEntityEvent import SingleEntityEvent
from ..ent.Weight import Weight
from ..math.Dist import Dist
import math

class GaussianEdgeEvent:
    
    """
    class GParam:
        def __init__(self,e,mean,stddev):
            self.e = e
            self.mean = mean
            self.stddev = stddev
    """

    def ex(mean, stddev): 
        return lambda e: e+abs(Dist.gaussian()*stddev+mean)
    #    #return lambda e: GaussianEdgeEvent.GParam(e,mean,stddev) 
    #    #return Weight => GParam = (e) => GParam(e, mean, stddev)

    #def ex(): 
    #    """return GParam => Weight = (bp) => bp.e + abs((Dist.gaussian())*bp.stddev + bp.mean)"""
    

    class GaussianContinuous(ContinuousEntityEvent):
        def __init__(self, uid, startingTime, variable, mean= 0.0, stddev=1.0):
            super().__init__(uid, startingTime, variable, GaussianEdgeEvent.ex(mean,stddev) ) #lambda e:e+abs(Dist.gaussian()*stddev+mean))#GaussianEdgeEvent.ex(mean,stddev))  #lambda x: print(x)) #lambda mean,stddev,e: e+abs(Dist.gaussian()*stddev+mean))
            """extends ContinuousEntityEvent[Weight](uid, startingTime, variable)(stage(mean, stddev) andThen ex) {"""
            variable.bindEvent(uid)

    class GaussianSingle(SingleEntityEvent):
        def __init__(self, uid, startingTime, variable, mean=0.0, stddev=1.0):
            super().__init__(uid, startingTime, variable, GaussianEdgeEvent.ex(mean,stddev) ) #lambda e:e+abs(Dist.gaussian()*stddev+mean))#lambda mean,stddev,e: e+abs(Dist.gaussian()*stddev+mean))
            """SingleEntityEvent[Weight](uid, startingTime, variable)(stage(mean, stddev) andThen ex) {"""
            variable.bindEvent(uid)

"""
package models

import timeseries.ContinuousEntityEvent
import timeseries.SingleEntityEvent
import ent.Weight
import math.Dist

object GaussianEdgeEvent {
  case class GParam(e: Weight, mean: Double, stddev: Double)

  def stage(mean: Double, stddev: Double): Weight => GParam = (e) => GParam(e, mean, stddev)
  def ex: GParam => Weight = (bp) => bp.e + Math.abs((Dist.gaussian)*bp.stddev + bp.mean)

  class GaussianContinuous(uid: Int, startingTime: Int, variable: Weight, mean: Double = 0.0, stddev: Double = 1.0)
    extends ContinuousEntityEvent[Weight](uid, startingTime, variable)(stage(mean, stddev) andThen ex) {
    variable.bindEvent(uid)
  }

  class GaussianSingle(uid: Int, startingTime: Int, variable: Weight, mean: Double = 0.0, stddev: Double = 1.0)
    extends SingleEntityEvent[Weight](uid, startingTime, variable)(stage(mean, stddev) andThen ex) {
    variable.bindEvent(uid)
  }
}
"""