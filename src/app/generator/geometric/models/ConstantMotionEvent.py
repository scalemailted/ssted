from ..timeseries.ContinuousEntityEvent import ContinuousEntityEvent
from ..ent.Point import Point

class ConstantMotionEvent:
    class Linear(ContinuousEntityEvent):
        def __init__(self, uid, startingTime, startingValue, velocity):
            super().__init__(uid, startingTime, startingValue, lambda x: x+velocity)
            startingValue.bindEvent(uid)


"""
package models

import timeseries.ContinuousEntityEvent
import ent.Point

object ConstantMotionEvent {
  class Linear(uid: Int, startingTime: Int, startingValue: Point, velocity: Seq[Double])
    extends ContinuousEntityEvent[Point](uid, startingTime, startingValue)((p) => p + velocity) {
    startingValue.bindEvent(uid)
  }
}
"""