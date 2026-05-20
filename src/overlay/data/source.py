from abc import ABC, abstractmethod

class DataSource(ABC):

    @abstractmethod
    def connect(self) -> bool:
        """try connecting with data source, return true if succeed."""

    
    @abstractmethod
    def disconnect(self) -> None:
        """disconnect from data source, if connected."""

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """check if connected with data source, return true if connected."""

    @abstractmethod
    def read_data(self) -> dict:
        """read data from data source, return a dictionary with the data.
            - speed_kmh: float
            - rpm: float
            - gear: int
            - rpm_max: float"""
