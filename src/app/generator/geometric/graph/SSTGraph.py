from ..graph.STNode import STNode 
from ..graph.STGraph import STGraph
from ..ent.Point import Point
from ..models.GaussianMotionEvent import GaussianMotionEvent
from ..models.GlobalEdgeConnectivityEvent import GlobalEdgeConnectivityEvent
from ..timeseries.TimeSeries import TimeSeries

#import scala.collection.mutable

"""
Specifies a Stochastic SpatioTemporal Graph with the given parameters
"""
class SSTGraph:
    def __init__(self, nodeIds, positions, nodeMeans, nodeStdDevs, r, muW, sigmaW):
        self.nodeIds = list(set(nodeIds))
        self.positions = positions
        self.nodeMeans = nodeMeans
        self.nodeStdDevs = nodeStdDevs
        self.r = r
        self.muW = muW
        self.sigmaW = sigmaW

    def getNodeIds(self):
        return self.nodeIds

    def getSTGraph(self):
        #stNodesMap = {}     #new mutable.HashMap[String,STNode]()
        ts = TimeSeries()

        nodeList = []
        for i in range(0, len(self.nodeIds)):
            pos = Point( *self.positions[i] ) #Point(positions(i).map(identity):_*)
            #print('\npoint', pos, id(pos))
            motion = GaussianMotionEvent.Continuous(ts.generateNextUID(), 0, pos, self.nodeMeans[i], self.nodeStdDevs[i])
            node = STNode(self.nodeIds[i], pos)
            #stNodesMap[self.nodeIds[i]] = node
            #print('[SSTGRAPH] motion', motion)
            nodeList.append(node)
            ts.addNodeMovementEvent(motion)

        #g = STGraph( list(stNodesMap.values()), [], ts)
        g = STGraph( nodeList, [], ts)
        ts.addGlobalEvent( GlobalEdgeConnectivityEvent.ContinuousGlobalRadio(ts.generateNextUID(), 0, g, self.r, self.muW, self.sigmaW))
        return g


