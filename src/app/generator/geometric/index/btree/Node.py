package index.btree

import scala.collection.mutable

/**
  * Represents a B-Tree node
  */
abstract class Node[T](slots: Int){
  val b = slots
  var m: Int = 0
  val keys = new mutable.ArraySeq[Long](b)
  var children = new mutable.ArraySeq[T](b)
  var next: Node[_] = null
  var parent: DirectoryNode = null

  def isFull = m == b

  def construct: Node[T]

  def split: Node[T] = {
    val rn = this.construct

    for ( index <- m/2 until m ) {
      rn.insert(children(index), keys(index))

      m -= 1
    }

    rn.parent = parent
    next = rn
    rn
  }

  def insert(item: T, key: Long): Int = {
    //TODO: this could be replaced with insertion type since it's sorted
    var insertionIndex = if ( m == 0 ) 0 else keys.view(0, m+1).indexWhere(_ > key)
    if ( insertionIndex == -1 ) insertionIndex = m

    for ( index <- m until insertionIndex by -1 ) {
      keys(index) = keys(index-1)
      children(index) = children(index-1)
    }

    keys(insertionIndex) = key
    children(insertionIndex) = item
    m += 1

    insertionIndex
  }

  def search(key: Long): Option[T] = {
    val index = keys.view(0, m+1).indexOf(key)

    return if (index == -1) None else new Some(children(keys.indexOf(key)))
  }
}
