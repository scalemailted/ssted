import numpy as np

#Various statistical mathematics
class Statistics:
    def getMean(arr):
        return np.mean(arr)

    def getVariance(arr):
        return np.var(arr)

    def getStdDev(arr):
        return np.std(arr)


"""
package math

import scala.math
import Numeric.Implicits._

/**
  * Various statistical mathematics
  */
object Statistics {
  def getMean[T: Numeric](iter: Iterable[T]): Double = iter.sum.toDouble / iter.size

  def getVariance[T: Numeric](iter: Iterable[T]): Double = {
    val m = getMean(iter)
    iter.map(_.toDouble).map(a => math.pow(a - m, 2)).sum / iter.size
  }

  def getStdDev[T: Numeric](iter: Iterable[T]): Double = {
    val m = getMean(iter)
    math.sqrt(iter.map(_.toDouble).map(a => math.pow(a - m, 2)).sum /(iter.size-1))
  }
}
"""
