package index.btree

class BTree[T](branchingFactor: Int) {
  val b: Int = branchingFactor
  var root: Node[_] = new DataNode[T](b)

  def insert(item: T, key: Long): Unit = {
    root match {
      case dataNode: DataNode[T] =>
        insertIntoDataNode(dataNode, item, key)
      case directoryNode: DirectoryNode =>
        insertIntoDirectoryNode(directoryNode, item, key)
    }
  }

  def insertIntoDirectoryNode(node: DirectoryNode, item: T, key: Long): Unit = {
    val insertionNode = BTree.search[T](key, node)
    insertIntoDataNode(insertionNode, item, key)
  }

  def insertIntoDataNode(node: DataNode[T], item: T, key: Long): Unit = {
    if ( node.m == node.b ) {
      val parent = splitNode(node)
      insertIntoDirectoryNode(parent, item, key)
    } else {
      node.insert(item, key)
      updateParentDirectories(node, key)
    }
  }

  def updateParentDirectories(node: Node[_], key: Long): Unit = {
    if ( node.parent == null ) return

    if ( node.keys(0) == key ) {
      val parent = node.parent
      val nodeIndex = parent.children.indexOf(node)
      if ( parent.keys(nodeIndex) != key ) {
        parent.keys(nodeIndex) = key

        updateParentDirectories(parent, key)
      }
    }
  }

  def splitNode(node: Node[_]): DirectoryNode = {
    if ( node.parent == null ) {
      val newNode = node.split
      val newRoot = new DirectoryNode(b)
      newRoot.insert(node)
      newRoot.insert(newNode)
      node.parent = newRoot
      newNode.parent = newRoot
      root = newRoot.asInstanceOf[Node[_]]
    } else {
      if ( node.parent.isFull ) {
        splitNode(node.parent)
      }

      val newNode = node.split
      node.parent.insert(newNode)
    }

    node.parent
  }


  def search(key: Long): Option[T] = {
    val dataNode = BTree.search[T](key, root)
    dataNode.search(key)
  }
}

object BTree {
  def search[T](key: Long, node: Node[_]): DataNode[T] = {
    node match {
      case dataNode: DataNode[T] =>
        dataNode
      case directoryNode: DirectoryNode =>
        val m = node.m
        val keys = node.keys
        var insertionIndex = keys.view(0, m+1).indexWhere(_ > key)
        if ( insertionIndex == -1 ) insertionIndex = m-1
        else if ( insertionIndex > 0 ) insertionIndex -= 1

        search(key, directoryNode.children(insertionIndex))
    }
  }

}
