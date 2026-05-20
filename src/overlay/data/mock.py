import math
import time

from .source import DataSource

class MockDataSource(DataSource):
    


    def __init__(self):
        self._connected = False
        self._start_time = 0.0


    def connect(self) -> bool:
        self._connected = True
        self._start_time = time.time()
        return self._connected
    
    def disconnect(self) -> None:
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected
    
    def read_data(self) -> dict: 
        
        if not self._connected:
            raise ConnectionError("Not connected to data source.")
        
        elapsed_time = time.time() - self._start_time
        speed_kmh = (math.sin(elapsed_time) + 1) / 2 * 200
        rpm = (math.sin(elapsed_time + math.pi / 2) + 1) / 2 * 8000
        gear = int((elapsed_time // 5) % 6) + 1
        rpm_max = 8000

        return {
            "speed_kmh": speed_kmh,
            "rpm": rpm,
            "gear": gear,
            "rpm_max": rpm_max
        }