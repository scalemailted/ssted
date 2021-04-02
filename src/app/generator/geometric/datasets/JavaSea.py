package datasets

import java.io.File

import scala.collection.mutable.HashMap
import scala.collection.mutable.ListBuffer
import scala.collection.mutable.HashSet
import scala.xml.XML
import graph.STNode
import graph.TEdge
import models.{EdgePathEvent, MotionPathEvent}
import timeseries.TimeSeries
import ent.Weight
import ent.Point

case class EdgePair(srcId: String, dstId: String)

object JavaSea {
  def loadGraph: (Set[STNode], Set[TEdge], TimeSeries) = {
    val directory = new File("C:\\Users\\cmichael\\IdeaProjects\\sst\\data\\JavaSea")
    val files = directory.listFiles.sortWith(_.getName < _.getName)

    val nodesHash = new HashMap[String, ListBuffer[Point]]()
    val edgesHash = new HashMap[EdgePair, ListBuffer[Weight]]()

    val stNodes = new HashSet[STNode]()
    val tEdges = new HashSet[TEdge]()

    val timeSeries = new TimeSeries
    var timeStep = 0

    var prevTouchedNodes = new HashSet[String]()
    var prevTouchedEdges = new HashSet[EdgePair]()

    def newEdgePathEvent(edge: EdgePair) = {
      val edgeId = edge.srcId+":"+edge.dstId

      //Find the edge object to send to event for side-effect update
      val tEdge = tEdges.find(_ == new TEdge(edgeId, edge.srcId, edge.dstId)).get
      val edgePath = edgesHash.get(edge).get
      val endTimeStep = timeStep - 1
      val startTimeStep = endTimeStep - edgePath.size + 1

      val pathEvent = new EdgePathEvent.Absolute(timeSeries.generateNextUID, startTimeStep, tEdge.weight, edgePath)
      timeSeries.addEdgeWeightEvent(pathEvent)
    }

    def newNodePathEvent(node: String) = {
      val stNode = stNodes.find(_ == new STNode(node)).get
      val nodePath = nodesHash.get(node).get
      val endTimeStep = timeStep - 1
      val startTimeStep = endTimeStep - nodePath.size + 1

      val pathEvent = new MotionPathEvent.Absolute(timeSeries.generateNextUID, startTimeStep, stNode.position, nodePath)
      timeSeries.addNodeMovementEvent(pathEvent)
    }

    for ( file <- files ) {
      val ss = XML.loadFile(file)

      val touchedNodes = new HashSet[String]()
      val touchedEdges = new HashSet[EdgePair]()

      for {
        nodeSS <- ss \\ "node"
      } yield {
        val nodeId = nodeSS \@ "id"
        val attrs = (nodeSS \ "data") map (key => key.attributes.value.text -> key.text) toMap
        val pos = new Point((attrs get "location_latitude" getOrElse "0.0" toDouble),
                            (attrs get "location_longitude" getOrElse "0.0" toDouble),
                            (attrs get "location_z" getOrElse "0.0" toDouble))
        (nodesHash getOrElseUpdate (nodeId, new ListBuffer[Point])) += pos
        stNodes += new STNode(nodeId, new Point(0.0, 0.0, 0.0))

        touchedNodes += nodeId
      }

      for {
        edgeSS <- ss \\ "edge"
      } yield {
        val attrs = (edgeSS \ "data") map (key => key.attributes.value.text -> key.text) toMap
        val source = edgeSS \@ "source"
        val target = edgeSS \@ "target"
        val edgeId = EdgePair(source, target)
        val weight = new Weight(attrs get "linkSuccessRate" getOrElse "0.0" toDouble)

        (edgesHash getOrElseUpdate (edgeId, new ListBuffer[Weight])) += weight
        tEdges += new TEdge(source+":"+target, source, target, new Weight(0.0))

        touchedEdges += edgeId
      }

      //Lost nodes (There are none in JavaSea)
      for ( node <- (prevTouchedNodes &~ touchedNodes) ) {
        newNodePathEvent(node)
      }

      //Lost edges
      for ( edge <- (prevTouchedEdges &~ touchedEdges) ) {
        newEdgePathEvent(edge)
      }

      prevTouchedNodes = touchedNodes
      prevTouchedEdges = touchedEdges

      timeStep += 1
    }

    prevTouchedNodes.map(newNodePathEvent(_))
    prevTouchedEdges.map(newEdgePathEvent(_))

    (stNodes.toSet, tEdges.toSet, timeSeries)
  }
}
