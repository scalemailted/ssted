class EventPool:
    def __init__(self):
        self.uIDStartTime = {}
        self.pool = {}
    
    def add(self, event):
        self.uIDStartTime[event.uid] = event.startTime
        if event.startTime in self.pool:                                     #pool.addBinding(event.startTime, event)
            self.pool[event.startTime].add(event)
        else:
            self.pool[event.startTime] = {event}
    
    def get(self, time):                                                     #Ted: changed t -> time
        return self.pool.get(time, None)
    
    def kill(self, uid):
        eventStartTime = self.uIDStartTime[uid]
        event = next((event for event in self.pool[eventStartTime] if event.uid == uid), None)   #event = pool[eventStartTime].find(_.getUID == uid)
        if event:
            self.pool[eventStartTime].remove(event)                         #pool.removeBinding(eventStartTime, event)
        #elif None: Unit
    
    def __str__(self):
        return "Event pool with "+str( len(self.pool) )+" Events"           #TODO: verify this for time count & not total event count, compare to scala result
    
    def stats(self):
        numEvents = 0 
        for it in self.pool.values():
            numEvents += len(it)
        ret = "EventPool total UIDs: " + str(len(self.uIDStartTime)) + " Events: " + str(numEvents) + "\n"
        return ret

