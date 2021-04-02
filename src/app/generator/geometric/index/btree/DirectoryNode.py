package index.btree

class DirectoryNode(elements: Int) extends Node[Node[_]](elements) {
  override def construct: DirectoryNode = new DirectoryNode(elements)

  def insert(item: Node[_]): Int = {
    val insertionIndex = insert(item, item.keys(0))
    item.parent = this

    if ( insertionIndex > 0 ) children(insertionIndex-1).next = children(insertionIndex)
    if ( insertionIndex < m-1 ) children(insertionIndex).next = children(insertionIndex+1)

    insertionIndex
  }

  override def split: DirectoryNode= {
    val rn = this.construct

    for ( index <- m/2 until m ) {
      rn.insert(children(index))

      m -= 1
    }

    rn.parent = parent
    next = rn
    rn
  }
}