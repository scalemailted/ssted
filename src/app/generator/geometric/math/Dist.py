import random

#Various statistical distributions
class Dist:
    def gaussian(mean=0, stdDev=1):                        #Static method, default parameters (Scala)
        return random.normalvariate(mean, stdDev)


"""
package math

import scala.util.Random

/**
  * Various statistical distributions
  */
object Dist {
  def gaussian : Double = Random.nextGaussian

  def gaussian(mean: Double, stdDev: Double) : Double = {
    Random.nextGaussian*stdDev + mean
  }
}
"""
