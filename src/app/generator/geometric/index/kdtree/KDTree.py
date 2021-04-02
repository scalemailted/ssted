#from ..graph.Spatial import Spatial

class Node:
    def __init__(self, dim, splitPoint, l, r, v):
        self.dim = dim
        self.splitPoint = splitPoint
        self.l = l
        self.r = r
        self.v = v

    def flatten(self,d):
      for i in d:
        yield from [i] if not isinstance(i, tuple) else self.flatten(i)
    
    #Bounding box range query.
    def rangeQuery(self, min, max):
        a = self.v.getPos().mags[self.dim] >= min[self.dim]
        b = self.v.getPos().mags[self.dim] <= max[self.dim]
        if a == True and b == True:
            if  self.v.getPos().isInBoundingBox(min, max): 
                result = (self.v,) + (self.l.rangeQuery(min, max),) + (self.r.rangeQuery(min, max),) #TED Tuples are dirty
                return tuple(self.flatten(result))
            else: 
                result = (self.l.rangeQuery(min, max),) + (self.r.rangeQuery(min, max),) #TED Tuples are dirty
                return tuple(self.flatten(result))
        elif a == False:
            result = (self.r.rangeQuery(min, max),) #TED Tuples are dirty
            return tuple(self.flatten(result))
        elif b == False:
            result = (self.l.rangeQuery(min, max),) #TED Tuples are dirty
            return tuple(self.flatten(result))
    
    def print(self, level=0): 
        return str(level) + ": " + str(self.v) + "\n" + self.l.print(level+1) + self.r.print(level+1)

class EmptyNode:
    def rangeQuery(self, min, max): 
        return () #None                       #TED Tuples are dirty
    def print(self, level= 0): 
        return str(level) + ": EmptyNode\n"

#A simple and unoptimized kd tree, mainly used now for bounding-box-ranged searches


#class KDTree:
#    def rangeQuery(self, min, max):
#        """must implement range query"""
#    def print(level: Int = 0): String


#class KDTree:
def build(d, points):
    #print('d',d,'points', ",".join(map(str,points)))
    if not points:
        #print('base-case')
        return EmptyNode()
    else:
        #print('recursive-case')
        sortedPoints = sorted(points, key=lambda x: x.getPos().mags[d])  #points.sort(key=lambda x: x.mags[d])  
        i = len(points)//2
        #print("sorted: ",",".join(map(str,sortedPoints)), "i:", i)
        medianPoint = sortedPoints[i]
        d_n = (d + 1) % len(medianPoint.getPos().mags)
        #print('dim:',d, 'split:',medianPoint.getPos().mags[d], 'left:',build(d_n, sortedPoints[:i]), 'right:',build(d_n, sortedPoints[i+1:] ), 'v',medianPoint)
        return Node(d, medianPoint.getPos().mags[d], build(d_n, sortedPoints[:i]), build(d_n, sortedPoints[i+1:] ), medianPoint)




"""
package index.kdtree

import graph.Spatial

import scala.collection.immutable.List

case class Node[T <: Spatial](
  final val dim: Int,
  final val splitPoint: Double,
  final val l: KDTree[T],
  final val r: KDTree[T],
  final val v: T)
 extends KDTree[T] {

  //Bounding box range query.
  def rangeQuery(min: List[Double], max: List[Double]): List[T] = {
    (v.getPos.mags(dim) >= min(dim), v.getPos.mags(dim) <= max(dim)) match {
      case (a,b) if ( a == true && b == true ) => {
        if ( v.getPos.isInBoundingBox(min, max) ) List(v) ++ l.rangeQuery(min, max) ++ r.rangeQuery(min, max)
        else l.rangeQuery(min, max) ++ r.rangeQuery(min, max)
      }
      case (a,_) if ( a == false )       => r.rangeQuery(min, max)
      case (_,b) if ( b == false )       => l.rangeQuery(min, max)
    }
  }

  def print(level: Int = 0): String = "" + level + ": " + v.toString() + "\n" + l.print(level+1) + r.print(level+1)
}

class EmptyNode[T] extends KDTree[T] {
  def rangeQuery(min: List[Double], max: List[Double]): List[T] = Nil

  def print(level: Int = 0): String = "" + level + ": EmptyNode\n"
}

/**
  * A simple and unoptimized kd tree, mainly used now for bounding-box-ranged searches
  */
sealed trait KDTree[T] {
  def rangeQuery(min: List[Double], max: List[Double]): List[T]

  def print(level: Int = 0): String
}

object KDTree {
  def build[T <: Spatial](d: Int, points: Seq[T]): KDTree[T] = {
    points match {
      case Nil => new EmptyNode //Is there a way to use one instance?
      case _ => {
        val sortedPoints = points.sortBy(_.getPos.mags(d))
        val i = points.size/2
        val medianPoint = sortedPoints(i)
        val d_n = (d + 1) % medianPoint.getPos.mags.size
        Node[T](d,
                medianPoint.getPos.mags(d),
                build(d_n, sortedPoints.slice(0,i)),
                build(d_n, sortedPoints.slice(i+1,points.size)),
                medianPoint)
      }
    }
  }

}
"""
