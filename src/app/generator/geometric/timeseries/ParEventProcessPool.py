from ..timeseries.EventProcessPool import EventProcessPool

class ParEventProcessPool(EventProcessPool):
    #This class uses a parrallelized hashmap in event process pool, which python does not support

    #TODO TED fix
    """
    def go(self):
            print("Performing processes")
            parPool = pool.par.map( r => {
                var v:Option[Iterator[_]] = None

                if ( r._2.isDefined && r._2.get.hasNext ) {
                    r._2.get.next()
                    v = r._2
                } 
                else {
                    v = None
                }

                r._1 -> v
            })

            print("Filtering processes")
            val filteredParPool = parPool.filter( r => r._2 != None)

            print("Finalizing processes")

            pool = filteredParPool.seq
    """
