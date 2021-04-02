package index.btree

class DataNode[T](elements: Int) extends Node[T](elements) {
  override def construct: DataNode[T] = new DataNode[T](elements)
}
