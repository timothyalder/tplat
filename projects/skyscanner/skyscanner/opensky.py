import time
import requests
from dataclasses import dataclass
from typing import List, Callable, Union

from skyscanner.roi import Sector, Rectangle


@dataclass
class FlightData:
    callsign: str
    origin: str | None
    destination: str | None
    make: str | None
    manufacturer: str | None

def _query_opensky(lamin: float, lomin: float, lamax: float, lomax: float):
    request = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
    response = requests.get(request, timeout=10)
    response.raise_for_status()
    return response.json()


def _extract_flights(data: dict) -> List[FlightData]:
    flights = []

    states = data.get("states", [])
    if not states:
        return flights
    
    for state in states:
        flights.append(
            FlightData(
                callsign=(state[1] or "").strip(),
                origin=None,
                destination=None,
                make=None,
                manufacturer=None,
            )
        )
    
    return flights


def start_query_loop(
    roi: Union[Sector, Rectangle],
    callback: Callable[[List[FlightData]], None],
    update_interval: int = 60,
):
    """
    Poll OpenSky every update_interval seconds and invoke callback
    with flights currently overhead.
    """

    while True:
        try:
            data = _query_opensky(lamin=roi.lamin, lomin=roi.lomin, lamax=roi.lamax, lomax=roi.lomax)
            flights = _extract_flights(data)
            callback(flights)
        except Exception as e:
            print(f"[WARN] OpenSky query failed: {e}")

        time.sleep(update_interval)
