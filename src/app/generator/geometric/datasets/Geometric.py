import os
import random
from ..graph.SSTGraph import SSTGraph
from ..analysis.SSTLCPS import lcps

"""
* d: number of dimensions
* n: number of nodes
* r: geometric range
* muN, sigmaN: min,max tuples for node movement
* muW, sigmaW: min,max tuples for weight variation
"""
def loadSSTGraph(d, n, r, muN, sigmaN, muW, sigmaW):
    nodeIds = []    #[new ArrayBuffer[String]()]
    positions = []    #new ArrayBuffer[Seq[Double]]()
    posMap = {}       #new mutable.HashMap[String,Seq[Double]]()
    nodeMeans =  []   #new ArrayBuffer[Double]()
    nodeStdDevs = []  #new ArrayBuffer[Double]()

    for i  in range( 0, n ):
        pos =  [random.uniform(0,100) for x in range(d)]        #Seq.fill(d)(Random.nextDouble*100)
        motionMean =    random.uniform(*muN)                      #getRandomInRange(muN._1, muN._2)
        motionStdDev =  random.uniform(*sigmaN)                 #getRandomInRange(sigmaN._1, sigmaN._2)

        nodeIds.append(str(i))
        positions.append(pos)
        posMap[str(i)] = pos
        nodeMeans.append(motionMean)
        nodeStdDevs.append(motionStdDev)

    return SSTGraph(nodeIds, positions, nodeMeans, nodeStdDevs, r, muW, sigmaW)



def buildNodeMovementDataset(r=20.0, nodes=50, duration=30, std=1.0, mean=0.0):
    #r = 20.0
    #nodes = 50
    experiments = 1
    #duration = 30

    sets = 0

    for stddev in [std]: #[1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0]:
        for i in range(0, experiments):
            sst = loadSSTGraph(2, nodes, r, (0.0,0.0), (0.0,stddev), (0.0,0.0), (0.0,mean))
            st = sst.getSTGraph()
            #print('\n\n#################  BEGINNING  ###############\n\n')
            #for n in st.stgNodes:
            #        print('stgnode', n.position, id(n.position))
            #st.clock()

            dirName = f"out_node-{sets:02d}-{i:02d}"
            os.mkdir(dirName)

            for j in range(0, duration):
                st.clock()
                #print('=============================================[',j,']===============================================')
                #for n in st.stgNodes:
                #    print('[geometric for-loop, top] stgnode point', n.position, id(n.position))
                path = os.path.join(dirName, f"{j:02d}.dat")
                filedat = open(path,'w')
                print("Creating string with "+str(len(st.stgNodes))+" nodes and "+str(len(st.stgEdges))+" edges.")
                string = str(st)
                print("String "+str(len(string))+" created. Writing file")
                filedat.write(str(st))
                filedat.flush()
                filedat.close()

                print("File written")
                #for n in st.stgNodes:
                #    print('[geometric for-loop, bottom] stgnode point', n.position, id(n.position))
                #st.clock()
        sets += 1


def buildEdgeCongestionDataset():
    r = 20.0
    nodes = 50
    experiments = 1
    duration = 30

    sets = 0

    for stddev in [1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0]:
        for i in range(0, experiments):
            sst = loadSSTGraph(2, nodes, r, (0.0,0.0), (0.0,0.0), (0.0,0.0), (0.0,stddev))
            st = sst.getSTGraph()
            st.clock()

            dirName = f"out_edge-{sets:02d}-{i:02d}"
            os.mkdir(dirName)

            for j in range(0, duration):
                path = os.path.join(dirName, f"{j:02d}.dat")
                filedat = open(path,'w')
                filedat.write(str(st))
                filedat.flush()
                filedat.close()

                print("File written")
                st.clock()        
        sets += 1



def sensitivityToEdgeCongestion():
    r = 20.0
    hops = 30
    trials = 10
    nodes = 50
    experiments = 10

    for stddev in [1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0]:
        meanEfficiency = ""
        stddevEfficiency = ""
        meanSimilarity = ""

        for i in range(0, experiments):
            sst = loadSSTGraph(2, nodes, r, (0.0,0.0), (0.0,0.0), (0.0,0.0), (0.0,stddev))
            #res = SSTLCPS.lcps(sst, "0", hops, trials)
            res = lcps(sst, "0", hops, trials)
            #meanEfficiency += ""+res._3+","
            #stddevEfficiency += ""+res._4+","
            #meanSimilarity += ""+res._1+","
            meanEfficiency += ""+str(res[2])+","
            stddevEfficiency += ""+str(res[3])+","
            meanSimilarity += ""+str(res[0])+","

        #val mEWriter = new PrintWriter("seriesEME"+stddev+".dat")
        #mEWriter.write(meanEfficiency.dropRight(1))
        #mEWriter.close
        mEWriter = open("seriesEME"+str(stddev)+".dat",'w')
        mEWriter.write(meanEfficiency)
        mEWriter.flush()
        mEWriter.close()

        #val sEWriter = new PrintWriter("seriesESE"+stddev+".dat")
        #sEWriter.write(stddevEfficiency.dropRight(1))
        #sEWriter.close
        sEWriter = open("seriesESE"+str(stddev)+".dat",'w')
        sEWriter.write(stddevEfficiency)
        sEWriter.flush()
        sEWriter.close()

        #val mSWriter = new PrintWriter("seriesEMS"+stddev+".dat")
        #mSWriter.write(meanSimilarity.dropRight(1))
        #mSWriter.close
        mSWriter= open("seriesEMS"+str(stddev)+".dat",'w')
        mSWriter.write(meanSimilarity)
        mSWriter.flush()
        mSWriter.close()



"""
  def sensitivityToEdgeCongestion: Unit = {
    val r = 20.0
    val hops = 30
    val trials = 10
    val nodes = 50
    val experiments = 50

    for ( stddev <- Seq(1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0) ) {
      var meanEfficiency = ""
      var stddevEfficiency = ""
      var meanSimilarity = ""

      for ( i <- 0 until experiments ) {
        val sst = loadSSTGraph(2, nodes, r, (0.0,0.0), (0.0,0.0), (0.0,0.0), (0.0,stddev))
        val res = SSTLCPS.lcps(sst, "0", hops, trials)
        meanEfficiency += ""+res._3+","
        stddevEfficiency += ""+res._4+","
        meanSimilarity += ""+res._1+","
      }

      val mEWriter = new PrintWriter("seriesEME"+stddev+".dat")
      mEWriter.write(meanEfficiency.dropRight(1))
      mEWriter.close

      val sEWriter = new PrintWriter("seriesESE"+stddev+".dat")
      sEWriter.write(stddevEfficiency.dropRight(1))
      sEWriter.close

      val mSWriter = new PrintWriter("seriesEMS"+stddev+".dat")
      mSWriter.write(meanSimilarity.dropRight(1))
      mSWriter.close
    }

  }

  def sensitivityToNodeMovement: Unit = {
    val r = 20.0
    val hops = 30
    val trials = 10
    val nodes = 50
    val experiments = 50


    for ( stddev <- Seq(1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0) ) {
      var meanEfficiency = ""
      var stddevEfficiency = ""
      var meanSimilarity = ""

      for ( i <- 0 until experiments ) {
        val sst = loadSSTGraph(2, nodes, r, (0.0,0.0), (0.0,stddev), (0.0,0.0), (0.0,0.0))
        val res = SSTLCPS.lcps(sst, "0", hops, trials)
        meanEfficiency += ""+res._3+","
        stddevEfficiency += ""+res._4+","
        meanSimilarity += ""+res._1+","
      }

      val mEWriter = new PrintWriter("seriesME"+stddev+".dat")
      mEWriter.write(meanEfficiency.dropRight(1))
      mEWriter.close

      val sEWriter = new PrintWriter("seriesSE"+stddev+".dat")
      sEWriter.write(stddevEfficiency.dropRight(1))
      sEWriter.close

      val mSWriter = new PrintWriter("seriesMS"+stddev+".dat")
      mSWriter.write(meanSimilarity.dropRight(1))
      mSWriter.close
    }

  }
}


"""