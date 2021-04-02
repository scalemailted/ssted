package index.btree

import scala.annotation.tailrec
import scala.collection.{immutable, mutable}

/**
  * A locality hashing algorithm based on GeoHash.
  * An example template: 00011122001122001122 three dimensional 20-bit hash
  */
class LocalityHash[T](template: String) {
  val hashTable = new mutable.LongMap[mutable.HashSet[T]]()
  val depth = template.size
  val labels: String = template.distinct
  val numDims: Int = labels.length
  val counts: immutable.IndexedSeq[Int] = labels.map(l => template.count(_ == l))
  val spans: List[(Char, Int)] = getSpans(template)

  def countContiguous(s: String): Int = s.indexWhere(_ != s(0))

  def magnitudeHash(dim: Char, magnitude: Double): Long = {
    LocalityHash.hash(magnitude, counts(labels.indexOf(dim)))
  }

  def getSpans(str: String):List[(Char,Int)] = {
    if ( str.isEmpty ) Nil
    else (str(0), str.span(_ == str(0))._1.length) :: getSpans(str.span(_ == str(0))._2)
  }

  def getHash(position: immutable.Seq[Double]): Long = {
    val magnitudeHashes = position.zipWithIndex.map(p => magnitudeHash(labels(p._2), p._1))
    var hash: Long = 0
    val bitsRemaining = mutable.ArraySeq[Int](counts:_*)

    for ( span <- spans ) {
      val dimIndex = labels.indexOf(span._1)
      val width = span._2
      val shifted = magnitudeHashes(dimIndex) >> (bitsRemaining(dimIndex)-width)
      val masked = shifted & ((1 << width) - 1)

      hash = (hash << width) | masked
      bitsRemaining(dimIndex) -= width
    }

    hash
  }
}

object LocalityHash {
  @tailrec
  def hash(candidate: Double, depth: Int, hashCode: Long = 0, split: Double = 0.5, childWidth: Double = 0.5): Long = {
    if ( depth == 0 ) {
      hashCode
    } else if ( candidate <= split ) {
      hash(candidate, depth-1, hashCode << 1, split - childWidth/2.0, childWidth/2.0)
    } else {
      hash(candidate, depth-1, (hashCode << 1)|1L, split + childWidth/2.0, childWidth/2.0)
    }
  }

  @tailrec
  def precision(depth: Int, width: Double = 1.0): Double = {
    if ( depth == 0 ) {
      width
    } else {
      precision(depth-1, width/2)
    }
  }
}
