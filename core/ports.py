from abc import ABC, abstractmethod
from datetime import datetime

class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass

class EntropySource(ABC):
    @abstractmethod
    def gauss(self, mu: float, sigma: float) -> float:
        pass

    @abstractmethod
    def seed(self, val: int) -> None:
        pass
