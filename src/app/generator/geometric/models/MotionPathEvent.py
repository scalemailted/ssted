from ..timeseries.PathEntityEvent import PathEntityEvent
from ..ent.Point import Point

class MotionPathEvent:
  class Additive(PathEntityEvent):
    def __init__(self, uid, startingTime, variable, path):
      super().__init__(uid, startingTime, variable, path, lambda p,seq: p+seq)
      variable.bindEvent(uid)

  class Absolute(PathEntityEvent):
    def __init__(self, uid, startingTime, variable, path):
      super().__init__(uid, startingTime, variable, path, lambda p,seq:(p:=seq) )
      variable.bindEvent(uid)

"""
package models

import timeseries.PathEntityEvent
import ent.Point

object MotionPathEvent {
  class Additive(uid: Int, startingTime: Int, variable: Point, path: Seq[Point])
    extends PathEntityEvent[Point](uid, startingTime, variable, path)((p, seq) => p + seq) {
    variable.bindEvent(uid)
  }

  class Absolute(uid: Int, startingTime: Int, variable: Point, path: Seq[Point])
    extends PathEntityEvent[Point](uid, startingTime, variable, path)((p, seq) => p := seq) {
    variable.bindEvent(uid)
  }
}
"""
