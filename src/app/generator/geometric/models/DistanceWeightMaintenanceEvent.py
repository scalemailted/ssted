from ..ent.Point import Point 
from ..ent.Weight import Weight
from ..timeseries.ContinuousEntityEvent import ContinuousEntityEvent
import math
#import operator
#from scipy.spatial import distance

class DistanceWeightMaintenanceEvent:
    #class GParam(e, s, d):                  #e:weight, s:point, d:point
    
    #def stage(src, dst): Weight => GParam = (e) => GParam(e, src, dst)
    #def ex: GParam => Weight = (gp) => gp.e := Math.sqrt(gp.s.mags.zip(gp.d.mags).map((t) => Math.pow(t._1-t._2,2)).sum)
    def ex(src, dst):
        #return lambda e: ( e := math.sqrt(sum((v1 - v2) ** 2 for v1, v2 in zip(src.mags, dst.mags)))
        #return lambda e: (e := distance.euclidean(src.mags,dst.mags))
        return lambda e: (e := math.dist(src,dst))

    class Continuous(ContinuousEntityEvent):
        def __init__(self, uid, startingTime, variable, src, dst):
            super().__init__(uid, startingTime, variable, DistanceWeightMaintenanceEvent.ex(src,dst) )#(stage(src, dst) andThen ex)
            variable.bindEvent(uid)



"""
package models

import ent.{Point, Weight}
import timeseries.ContinuousEntityEvent

object DistanceWeightMaintenanceEvent {
  case class GParam(e: Weight, s: Point, d: Point)

  def stage(src: Point, dst: Point): Weight => GParam = (e) => GParam(e, src, dst)
  def ex: GParam => Weight = (gp) => gp.e := Math.sqrt(gp.s.mags.zip(gp.d.mags).map((t) => Math.pow(t._1-t._2,2)).sum)

  class Continuous(uid: Int, startingTime: Int, variable: Weight, src: Point, dst: Point)
    extends ContinuousEntityEvent[Weight](uid, startingTime, variable)(stage(src, dst) andThen ex) {
    variable.bindEvent(uid)
  }
}
"""