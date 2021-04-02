
"""
package graph

import scalax.collection.GraphEdge.{DiEdge, EdgeCopy, NodeProduct}
import scalax.collection.GraphPredef.OuterEdge

/**
  * Specifies a Temporal Aggregate edge for a time-aggregated type graph implementation
  */
case class TAEdge[+N](src: N, dst: N, w: Seq[Double])
 extends DiEdge[N](NodeProduct(src, dst)) with EdgeCopy[TAEdge] with OuterEdge[N, TAEdge] {
  private def this(nodes: Product, w: Seq[Double]) {
    this(nodes.productElement(0).asInstanceOf[N],
         nodes.productElement(1).asInstanceOf[N], w)
  }

  def keyAttributes = Seq(w)
  override def copy[NN](newNodes: Product) = new TAEdge[NN](newNodes, w)
  override protected def attributesToString = s" ($w)"

  def getWeight(t: Int) = w(t)
}

object TAEdge {
  implicit final class ImplicitEdge[A <: String](val e: DiEdge[String]) extends AnyVal {
  def ## (w: Seq[Double]) = new TAEdge(e.source, e.target, w)
  }
}
"""

