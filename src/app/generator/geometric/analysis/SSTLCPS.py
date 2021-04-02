from  ..graph.SSTGraph import SSTGraph
from  ..graph.STGraph import STGraph
from ..math.Statistics import Statistics

#Shortest path stability algorithms used in SSDBM Submission

#object SSTLCPS {

def jaccardIndex(a, b):
    #print('a',a,'b',b)
    intersection = a.intersection(b)
    union = a.union(b)
    if not union or len(union) == 0: 
        return 1.0
    else:
        return len(intersection) / len(union) 

#Should return avg of Jaccard index from source to destination for all trials
def lcps(graph, srcId, duration, trials):
    pathsTo = {}
    efficiencies = {}
    for trial in range (trials):
        g = graph.getSTGraph()
        g.clock() #Initializes the graph.
        delta, paths = tape(g, srcId, duration)

    for dst in set(graph.getNodeIds()) - set(srcId): #not use srcId
        if dst not in pathsTo:
            pathsTo[dst] = []
        if dst in paths:
            pathsTo[dst].append( set(paths[dst]) )
        else:  #Paths where the destination is unreachable will only contain the destination 
            pathsTo[dst].append( set(dst) )   

        if dst not in efficiencies:
            efficiencies[dst] = []
        
        efficiencies[dst].append( 1.0/ (delta.get(dst) or float('inf'))  ) #delta or float("inf")    
       
    aggJ = []

    for dst in pathsTo:
        aggJDst = 0.0
        i = len( pathsTo[dst][0] ) #TED --> dirty fix, see below for original version
        #i = len( pathsTo[dst])
        sets = [ (x,y) for x in range(i) for y in range(i) if x < y ]
        #print('pathsTo[dst]', pathsTo[dst])
        #print('i',i)
        #print('sets',sets)

        for coord in sets:
            #aggJDst += jaccardIndex(pathsTo[dst][coord[0]], pathsTo[dst][coord[1]])
            #print( pathsTo[dst][0],coord[0],coord[1] )
            #print( list(pathsTo[dst][0])[coord[0]], list(pathsTo[dst][0])[coord[1]])
            aggJDst += jaccardIndex(set(list(pathsTo[dst][0])[coord[0]]), set(list(pathsTo[dst][0])[coord[1]]))

        #aggJ += aggJDst / len(sets)
        aggJ.append( aggJDst / (len(sets) or 1) )

    allMeanEfficiencies = []
    allStdDevEfficiencies = []

    for dst in efficiencies:
        allMeanEfficiencies.append( Statistics.getMean(efficiencies[dst]) )
        allStdDevEfficiencies.append( Statistics.getStdDev(efficiencies[dst]) )

    print(pathsTo)
    return (Statistics.getMean(aggJ), Statistics.getStdDev(aggJ),
        Statistics.getMean(allMeanEfficiencies), Statistics.getStdDev(allStdDevEfficiencies))

def tape(graph, srcId, duration):
    print('SSTLCPS.tape')
    delta = {}
    path = {}

    delta[srcId] = 0.0
    path[srcId] = [srcId]

    for t in range(duration):
        graph.clock()
        g = graph.getGraph()

        for e in g.edges:
            source, target = e
            #print('graph g',g,type(g), g.edges, g[e[0]][e[1]])
            #print('SSTLCPS.tape', 'for-loop on graph edges','edge:',e, type(e), source, target)
            if source in delta:
                if delta.get(target) or float('inf')  > delta[source] + g[source][target]['weight']:
                    delta[target] = delta[source] + g[source][target]['weight']
                    path[target] = path[source] + [target]

    return (delta, path)

