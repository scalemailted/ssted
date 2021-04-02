from ..ent.Weight import Weight
from ..graph.STGraph import STGraph
from ..graph.TEdge import TEdge
from ..index.kdtree import KDTree  #import *
from ..timeseries.ContinuousGlobalEvent import ContinuousGlobalEvent
from .DistanceWeightMaintenanceEvent import DistanceWeightMaintenanceEvent
from .GaussianEdgeEvent import GaussianEdgeEvent

from random import random
import math
#from scipy.spatial import distance

#class ContinuousGlobalRadio (ContinuousGlobalEvent):
#    def __init__(self, uid, startingTime, graph, r, muW, sigmaW):
#        super().__init__(uid, startingTime, graph)
#        super.updateEdges(r, muW, sigmaW)


class GlobalEdgeConnectivityEvent:

    class ContinuousGlobalRadio (ContinuousGlobalEvent):
        def __init__(self, uid, startingTime, graph, r, muW, sigmaW):
            super().__init__(uid, startingTime, graph, lambda g:GlobalEdgeConnectivityEvent.updateEdges(r, muW, sigmaW, g))
            #GlobalEdgeConnectivityEvent.updateEdges(r, muW, sigmaW, graph)


    def getRandomInRange(min, max): 
        return random() * (max-min) + min

    def updateEdges(r, muW, sigmaW, g): 
        #STGraph => STGraph = {
        #(g) => {
        #print('--------------------------------------------[ updateEdges ]---------------------------------------')
        sgraph = g.getGraph()
        #print('sgraph', sgraph.size())
        bbNodesTree = KDTree.build(0, g.stgNodes)
        #print('bbNodesTree',bbNodesTree)

        nearbyNodesMap = {}
        for n in g.stgNodes:
            #min = list(n.getPos() - r)
            #max = list(n.getPos() + r)
            min = list( map(lambda x:x-r, n.getPos().mags ))
            max = list( map(lambda x:x+r, n.getPos().mags ))
            nearbyNodesMap[n] = bbNodesTree.rangeQuery(min,max)

        """
        nearbyNodesMap = g.stgNodes.par.map( n =>  {
            min = n.getPos().mags.map(_ - r).toList
            max = n.getPos().mags.map(_ + r).toList
            n -> bbNodesTree.rangeQuery(min, max)
        }).toMap
        """

        for src in g.stgNodes:
            #print('src', src)
            bbNodes = set(nearbyNodesMap[src])
            #print('\t bbNodes', len(bbNodes))
            #print('\tbbnodes', list(bbNodes) )
            #for i in bbNodes:
            #    print('\t\tnode:',i)



            #Find edges that are not in the neighborhood and remove them.
            #for currentNeighborUID in sgraph.get(src.uid).diSuccessors.map(_.toOuter):
            for currentNeighborUID in sgraph.successors(src.uid):
                currentNeighborEdgeUID = src.uid + ":" + currentNeighborUID
                #print( g.stgNodesMap, currentNeighborUID)
                if not g.stgNodesMap[currentNeighborUID] in list(bbNodes) and g.hasEdge(currentNeighborEdgeUID):
                    g.removeEdge(currentNeighborEdgeUID) #//Side Effect

            #For all neighborhood nodes
            #print(bbNodes, src)
            #print( '\t bbnodes - src =',len(bbNodes.difference({src})))

            for dst in bbNodes.difference({src}):
                if isinstance(dst, tuple):
                    #print('\t\t instance tuple')
                    continue
                #print('\t\t dst', dst)
                distance = math.dist(src.getPos().mags, dst.getPos().mags)
                #print('DISTANCE', distance)
                #distance = distance.euclidean(src.getPos().mags, dst.getPos().mags) #distance = math.sqrt(src.getPos.mags.zip(dst.getPos.mags).map(t => Math.pow(t._1-t._2,2)).sum)
                edgeUID = str(src.uid)+":"+str(dst.uid)
                #print('\t\t edgeUID', edgeUID)

                if distance > r and g.hasEdge(edgeUID):         #//The dest node is out of range.  Remove it.
                    g.removeEdge(edgeUID)                       #//Side effect
                elif distance <= r and not g.hasEdge(edgeUID):  #//A new node is in range.  Add an edge.
                    w = Weight(distance)
                    e = TEdge(edgeUID, src.uid, dst.uid, w)
                    #//Notice the g.ts.ctr.  It is OK to insert these events at the current time because global events
                    #// get processed before maintenance and weight events (but after move events).
                    m = DistanceWeightMaintenanceEvent.Continuous(g.ts.generateNextUID(), g.ts.ctr, w, src.getPos(), dst.getPos())
                    ev = GaussianEdgeEvent.GaussianContinuous(g.ts.generateNextUID(), g.ts.ctr, w, GlobalEdgeConnectivityEvent.getRandomInRange(muW[0], muW[1]), GlobalEdgeConnectivityEvent.getRandomInRange(sigmaW[0], sigmaW[1]))

                    g.addEdge(e)                    #//Side effects
                    g.ts.addMaintenance(m)          #//Side effects
                    g.ts.addEdgeWeightEvent(ev)     #//Side effects

        return g



"""
  * This object is a hack at getting the Geometric Random SST graph edge connectivity working properly.
  * Edge connectivity should not have to be a global event.
"""

#TODO TED fix -- Scala Case Class in Python

"""
object GlobalEdgeConnectivityEvent {
  private def getRandomInRange(min: Double, max:Double): Double = Random.nextDouble*(max-min)+min

  def updateEdges(r: Double, muW: (Double, Double), sigmaW: (Double, Double)): STGraph => STGraph = {
    (g) => {
      val sgraph = g.getGraph

      val bbNodesTree = KDTree.build(0, g.stgNodes.toSeq)

      val nearbyNodesMap = g.stgNodes.par.map( n =>  {
        val min = n.getPos.mags.map(_ - r).toList
        val max = n.getPos.mags.map(_ + r).toList
        n -> bbNodesTree.rangeQuery(min, max)
      }).toMap

      for ( src <- g.stgNodes ) {
        val bbNodes = nearbyNodesMap(src).toSet

        //Find edges that are not in the neighborhood and remove them.
        for ( currentNeighborUID <- sgraph.get(src.uid).diSuccessors.map(_.toOuter) ) {
          val currentNeighborEdgeUID = src.uid + ":" + currentNeighborUID

          if ( !bbNodes.contains(g.stgNodesMap(currentNeighborUID)) &&  g.hasEdge(currentNeighborEdgeUID) ) {
            g.removeEdge(currentNeighborEdgeUID) //Side Effect
          }
        }

        //For all neighborhood nodes
        for ( dst <- bbNodes - src ) {
          val distance = Math.sqrt(src.getPos.mags.zip(dst.getPos.mags).map(t => Math.pow(t._1-t._2,2)).sum)
          val edgeUID = src.uid+":"+dst.uid

          if ( distance > r && g.hasEdge(edgeUID) ) { //The dest node is out of range.  Remove it.
            g.removeEdge(edgeUID) //Side effect
          } else if ( distance <= r && !g.hasEdge(edgeUID) ) { //A new node is in range.  Add an edge.
            val w = new Weight(distance)

            val e = new TEdge(edgeUID, src.uid, dst.uid, w)

            //Notice the g.ts.ctr.  It is OK to insert these events at the current time because global events
            // get processed before maintenance and weight events (but after move events).
            val m =
             new DistanceWeightMaintenanceEvent.Continuous(g.ts.generateNextUID, g.ts.ctr, w, src.getPos, dst.getPos)

            val ev = new GaussianEdgeEvent.GaussianContinuous(g.ts.generateNextUID, g.ts.ctr, w,
              getRandomInRange(muW._1, muW._2), getRandomInRange(sigmaW._1, sigmaW._2))

             g.addEdge(e) //Side effects
             g.ts.addMaintenance(m) //Side effects
             g.ts.addEdgeWeightEvent(ev) //Side effects
          }

        }
      }
    }

    g
  }
"""