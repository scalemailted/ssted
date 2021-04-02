from abc import ABC, abstractmethod

#Entities are containers for side-effected variables.
class Entity(ABC):

    #Add, then return the sum entity
    @abstractmethod
    def __add__(self, other):
        """overload (+) plus operator."""

    #Binds and unbinds the entity to the given event UID
    @abstractmethod
    def bindEvent(self, uid):
        """This method should bind event given uid."""
   
    @abstractmethod
    def unbindEvent(self, uid):
        """This method should unbind event given uid."""

    @abstractmethod
    def getBindings(self):
        """This method return the set of bindings."""
    
    def __hash__(self):
        return super().__hash__()


"""
/**
  * 
  */
trait Entity[T <: Entity[T]] {
    //Add, then return the sum entity
    def +(that: T): T

    //Assign, then return the updated entity
    def :=(that: T): T

    //Binds and unbinds the entity to the given event UID
    def bindEvent(uid: Int)
    def unbindEvent(uid: Int)
    def getBindings: Set[Int]
}
"""
