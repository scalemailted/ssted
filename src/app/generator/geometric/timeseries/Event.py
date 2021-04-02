from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Event(ABC):
    @abstractmethod
    def getStartTime(self) -> int:
        pass
    @abstractmethod
    def getIter(self) -> int:
        pass
    @abstractmethod
    def getUID(self) -> int:
        pass


"""
package timeseries

trait Event {
  def getStartTime: Int
  def getIter: Iterator[_]
  def getUID: Int
}
"""