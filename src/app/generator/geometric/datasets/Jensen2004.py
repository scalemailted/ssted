package datasets

import ent.Point
import graph.STNode
import models.ConstantMotionEvent
import timeseries.TimeSeries

import scala.collection.mutable
import scala.util.Random

object Jensen2004 {
  def loadGraph(movingObjects: Int = 10000,
                spaceDomain: Seq[Int] = Seq(1000,1000),
                speedRange: (Double,Double) = (0.0,3.0)) = {
    val spatialD = spaceDomain.size

    val stNodes = new mutable.HashSet[STNode]()
    val timeSeries = new TimeSeries

    for ( i <- 0 until movingObjects ) {
      val initialPos = new Point(Seq.fill(spatialD)(Random.nextDouble):_*)
      val velocity = Seq.fill(spatialD)(Random.nextDouble*(speedRange._2-speedRange._1)+speedRange._1)
      val motionEvent = new ConstantMotionEvent.Linear(timeSeries.generateNextUID, 0, initialPos, velocity)

      stNodes += new STNode(i.toString, initialPos)
      timeSeries.addNodeMovementEvent(motionEvent)
    }
  }

}
