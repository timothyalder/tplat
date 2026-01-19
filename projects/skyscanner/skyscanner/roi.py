from dataclasses import dataclass
from typing import Literal, Optional
import math
from abc import ABC, abstractmethod

class ROI(ABC):
    earth_radius_km = 6371.0
    
    @staticmethod
    def _km_to_deg_lat(km: float) -> float:
        return km / 110.574


    @staticmethod
    def _km_to_deg_lon(km: float, lat: float) -> float:
        return km / (111.320 * math.cos(math.radians(lat)))


    @staticmethod
    def _rotate(x: float, y: float, heading_deg: float) -> tuple[float, float]:
        """Rotate vector by heading (degrees, clockwise from north)."""
        theta = math.radians(heading_deg)
        xr = x * math.cos(theta) - y * math.sin(theta)
        yr = x * math.sin(theta) + y * math.cos(theta)
        return xr, yr
    
    @property
    @abstractmethod
    def lamin(self) -> float:
        ...
        
    @property
    @abstractmethod
    def lamax(self) -> float:
        ...
        
    @property
    @abstractmethod
    def lomin(self) -> float:
        ...
        
    @property
    @abstractmethod
    def lomax(self) -> float:
        ...
        

@dataclass
class Rectangle(ROI):
    origin_lat: float
    origin_lon: float
    heading: float
    width_km: float = 4.0
    depth_km: float = 2.0
    
    # Need to add rotation
    
    @property
    def lamin(self) -> float:
        return self.origin_lat

    @property
    def lamax(self) -> float:
        return self.origin_lat + self._km_to_deg_lat(self.depth_km)

    @property
    def lomin(self) -> float:
        half_width = self.width_km / 2
        return self.origin_lon - self._km_to_deg_lon(half_width, self.origin_lat)

    @property
    def lomax(self) -> float:
        half_width = self.width_km / 2
        return self.origin_lon + self._km_to_deg_lon(half_width, self.origin_lat)


@dataclass
class Sector(ROI):
    origin_lat: float
    origin_lon: float
    heading: float
    radius_km: float = 4.0
    angle_deg: float = 140.0
    
    @property
    def lamin(self) -> float:
        return self.origin_lat - self._km_to_deg_lat(self.radius_km)

    @property
    def lamax(self) -> float:
        return self.origin_lat + self._km_to_deg_lat(self.radius_km)

    @property
    def lomin(self) -> float:
        return self.origin_lon - self._km_to_deg_lon(self.radius_km, self.origin_lat)

    @property
    def lomax(self) -> float:
        return self.origin_lon + self._km_to_deg_lon(self.radius_km, self.origin_lat)



def define_roi(
    latitude: float,
    longitude: float,
    heading: float,
    width_km: Optional[float] = 50.0,
    depth_km: Optional[float] = 50.0,
    radius_km: Optional[float] = 4.0,
    angle_deg: Optional[float] = 140.0,
    shape: Literal["rectangle", "sector"] = "rectangle",
) -> ROI:
    if shape == "rectangle":
        return Rectangle(
            origin_lat=latitude,
            origin_lon=longitude,
            heading=heading,
            width_km=width_km,
            depth_km=depth_km,
        )

    elif shape == "sector":
        return Sector(
            origin_lat=latitude,
            origin_lon=longitude,
            heading=heading,
            radius_km=radius_km,
            angle_deg=angle_deg,
        )

    else:
        raise ValueError(f"Unsupported shape: {shape}")
