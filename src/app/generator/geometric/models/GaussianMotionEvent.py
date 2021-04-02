from dataclasses import dataclass
from ..timeseries.ContinuousEntityEvent import ContinuousEntityEvent
from ..timeseries.SingleEntityEvent import SingleEntityEvent
from ..ent.Point import Point
from ..math.Dist import Dist


class GaussianMotionEvent:

    #case class BParam(p: Point, mean: Double, stddev: Double)

    #def stage(mean: Double, stddev: Double): Point => BParam = (p) => BParam(p, mean, stddev)
    #def ex: BParam => Point = (bp) => bp.p +~ ((x) => x + (Dist.gaussian)*bp.stddev + bp.mean)
    def ex(mean, stddev):
        return lambda p: p + (Dist.gaussian()*stddev + mean)

    class Continuous(ContinuousEntityEvent):
        def __init__(self, uid, startingTime, startingValue, mean=0.0, stddev=1.0):
            super().__init__(uid, startingTime, startingValue, GaussianMotionEvent.ex(mean, stddev) )
            #extends ContinuousEntityEvent[Point](uid, startingTime, startingValue)(stage(mean, stddev) andThen ex)
            startingValue.bindEvent(uid)
            #print('GaussianMotionEvent Point', startingValue, id(startingValue))
            #(uid: Int, startingTime: Int, startingValue: Point, mean: Double = 0.0, stddev: Double = 1.0)
        
        
  

    class Single(SingleEntityEvent):
        def __init__(self, uid, startingTime, value, mean=0.0, stddev=1.0):
            super().__init__(uid, startingTime, value, GaussianMotionEvent.ex(mean, stddev) )
            #extends SingleEntityEvent[Point](uid, startingTime, value)(stage(mean, stddev) andThen ex) {
            value.bindEvent(uid)
  








#TODO TED fix:  Python equivalent of Scala case class
# https://stackoverflow.com/questions/51342228/python-equivalent-of-scala-case-class
"""
GaussianMotionEvent {

  case class BParam(p: Point, mean: Double, stddev: Double)

  def stage(mean: Double, stddev: Double): Point => BParam = (p) => BParam(p, mean, stddev)
  def ex: BParam => Point = (bp) => bp.p +~ ((x) => x + (Dist.gaussian)*bp.stddev + bp.mean)

  class Continuous(uid: Int, startingTime: Int, startingValue: Point, mean: Double = 0.0, stddev: Double = 1.0)
    extends ContinuousEntityEvent[Point](uid, startingTime, startingValue)(stage(mean, stddev) andThen ex) {
    startingValue.bindEvent(uid)
  }

  class Single(uid: Int, startingTime: Int, value: Point, mean: Double = 0.0, stddev: Double = 1.0)
    extends SingleEntityEvent[Point](uid, startingTime, value)(stage(mean, stddev) andThen ex) {
    value.bindEvent(uid)
  }
}
"""
