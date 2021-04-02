#TODO TED fix: find replacemment library for Scala Graphs. 
#from igraph import *                                #scala: scalax.collection.Graph
#from graphviz import *                              #scala: scalax.collection.io.dot
#> launch /usr/local/Cellar/graph-tool/2.31_1/libexec/bin/python3
#import sys
#sys.path.append('/usr/local/opt/graph-tool/lib/python3.8/site-packages/')
#from graph_tool.all import *

import networkx as nx
from ..timeseries.TimeSeries import TimeSeries
from .STNode import STNode
from .TEdge import TEdge

#  * Specifies a SpatioTemporal graph

class STGraph:
    def __init__(self, stNodes, tEdges, timeSeries):
        self.stgNodes =  set( stNodes )
        self.stgEdges = set( tEdges )
        self.ts = timeSeries
        self.stgNodesMap = {n.uid: n for n in self.stgNodes}
        self.stgEdgesMap = {e.uid: e for e in self.stgEdges}
        #print('\n\n#################  STGraph CONSTRUCTOR  ###############')
        #for n in self.stgNodes:
        #    print('self.stgnode', n.position, id(n.position))
    
    def clock(self, n=1):
        for i in range (n):
            self.ts.clockEvents()
    
    def getGraph(self):         #Graph[String, WDiEdge]
        nodes = [ stgNode.uid for stgNode in self.stgNodes ]
        edges = [ (stgEdge.src, stgEdge.dst, stgEdge.getWeight().mag) for stgEdge in self.stgEdges ]
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_weighted_edges_from(edges)
        #print('nodes',str(nodes))
        #print('edges',str(edges))
        #print('networx graph',graph.size())
        return graph
        """
        edges = []
        nodes = []
        for stgNode in self.stgNodes:
            nodes.append(stgNode.uid)

        for stgEdge in self.stgEdges:
            edges.append( (stgEdge.src, stgEdge.dst, stgEdge.getWeight().mag )  ) #WDiEdge(stgEdge.src, stgEdge.dst)(stgEdge.getWeight.mag)
        """
        #return Graph.from[String, WDiEdge](nodes, edges)

    def removeEdge(self, edgeUID):
        if edgeUID in self.stgEdgesMap:
            edge = self.stgEdgesMap[edgeUID]
            bindings = edge.getWeight().getBindings()
            for event in bindings:
                self.ts.killEvent(event)
            self.stgEdges.remove( self.stgEdgesMap[edgeUID] )
            del self.stgEdgesMap[edgeUID]

    def hasEdge(self, edgeUID):
        return edgeUID in self.stgEdgesMap

    def addEdge(self, edge):
        self.stgEdges.add(edge)
        self.stgEdgesMap[edge.uid] = edge

    def getDot(self):
        nx.drawing.nx_agraph.write_dot(self.getGraph(), str(self.ts.ctr))


    #Do not use this for graphs with high node and edge counts due to performance.
    def __str__(self):
        ret = ""
        for node in self.stgNodes: 
            ret += str(node) + "\n"
        for edge in self.stgEdges:
            ret += str(edge) + "\n"
        return ret

    def stats(self):
        ret = ""
        nodeBindingCount = 0;
        edgeBindingCount = 0;

        for node in self.stgNodes:
            nodeBindingCount += len(node.getPos().getBindings())
        for edge in self.stgEdges:
            edgeBindingCount += len(edge.getWeight().getBindings())

        ret += "Node bindings: "+nodeBindingCount+"; Edge bindings: "+edgeBindingCount+ "\n"
        ret += self.ts.stats()
        return ret



"""
import scalax.collection.Graph
import scalax.collection.edge.WDiEdge
import timeseries.TimeSeries
import scalax.collection.io.dot.{DotAttr, DotAttrStmt, DotEdgeStmt, DotGraph, DotNodeStmt, DotRootGraph, Elem, graph2DotExport}
import scalax.collection.io.dot.implicits._

import scala.collection.mutable


#  * Specifies a SpatioTemporal graph

class STGraph(stNodes: Seq[STNode], tEdges: Seq[TEdge], timeSeries: TimeSeries) {
  val stgNodes: mutable.Set[STNode] = stNodes.to[mutable.Set]
  val stgEdges: mutable.Set[TEdge] = tEdges.to[mutable.Set]
  val ts = timeSeries

  val stgNodesMap = mutable.HashMap[String, STNode](stNodes.map(n => (n.uid,n)): _*)
  val stgEdgesMap = mutable.HashMap[String, TEdge](tEdges.map(e => (e.uid,e)): _*)

  def clock(n:Int = 1) = {
    0 until n foreach {_ => ts.clock}
  }

  def getGraph: Graph[String, WDiEdge] = {
    val edges = new mutable.ListBuffer[WDiEdge[String]]
    val nodes = new mutable.ListBuffer[String]

    for ( stgNode <- stgNodes ) {
      nodes += stgNode.uid
    }
    for ( stgEdge <- stgEdges ) {
      edges += WDiEdge(stgEdge.src, stgEdge.dst)(stgEdge.getWeight.mag)
    }

    Graph.from[String, WDiEdge](nodes, edges)
  }

  def removeEdge(edgeUID: String) = {
    if ( stgEdgesMap.contains(edgeUID) ) {
      val edge = stgEdgesMap(edgeUID)
      val bindings = edge.getWeight.getBindings

      bindings.map(ts.killEvent(_))

      stgEdges -= stgEdgesMap(edgeUID)
      stgEdgesMap.remove(edgeUID)
    }
  }

  def hasEdge(edgeUID: String): Boolean = {
    stgEdgesMap.contains(edgeUID)
  }

  def addEdge(edge: TEdge) = {
    stgEdges += edge
    stgEdgesMap(edge.uid) = edge
  }



  def getDot: String = {
    val root = DotRootGraph( directed = true,
                             id = Some("time_"+ts.ctr.toString),
                             attrStmts = List(DotAttrStmt(Elem.node, List(DotAttr("label", "\"\\N\""))),
                             DotAttrStmt(Elem.graph, List(DotAttr("bb", "\"0,0,10,10\"")))))

    def edgeTransformer(innerEdge: Graph[String, WDiEdge]#EdgeT): Option[(DotGraph, DotEdgeStmt)] =
      Some((root, DotEdgeStmt(innerEdge.toOuter.source, innerEdge.toOuter.target,
           List(DotAttr("label", "\""+innerEdge.toOuter.weight.formatted("%.8f")+"\"")))))

    def nodeTransformer(innerNode: Graph[String, WDiEdge]#NodeT): Option[(DotGraph, DotNodeStmt)] = {
      Some((root, DotNodeStmt(innerNode.toOuter,
           List(DotAttr("pos", "\""+stgNodesMap(innerNode.toOuter).getPos.mags.map(_*10.0).mkString(",")
           +"!\"")))))
    }

    getGraph.toDot(root, edgeTransformer, None, Some(nodeTransformer), Some(nodeTransformer))
  }

  /**
    * Do not use this for graphs with high node and edge counts due to performance.
    */
  override def toString: String = {
    var ret = new StringBuilder(10000)

    for ( node <- stgNodes ) ret ++= node + "\n"
    for ( edge <- stgEdges ) ret ++= edge + "\n"

    ret.result
  }

  def stats: String = {
    val ret = new StringBuilder(1024)
    var nodeBindingCount = 0;
    var edgeBindingCount = 0;

    for ( node <- stgNodes ) nodeBindingCount += node.getPos.getBindings.size
    for ( edge <- stgEdges ) edgeBindingCount += edge.getWeight.getBindings.size

    ret ++= "Node bindings: "+nodeBindingCount+"; Edge bindings: "+edgeBindingCount+ "\n"

    ret ++= ts.stats

    ret.toString
  }
}
"""
