import time
import os
import requests
from dataclasses import dataclass
from typing import List, Callable, Union, Optional

from skyscanner.roi import Sector, Rectangle


@dataclass
class FlightData:
    callsign: str
    origin: str | None
    destination: str | None
    make: str | None
    manufacturer: str | None
    

def _auth_opensky():
    url = f"https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("OPENSKY_CLIENT_ID"),
        "client_secret": os.environ.get("OPENSKY_CLIENT_SECRET"),
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    token_data = response.json()
    access_token = token_data.get("access_token", None)
    return access_token


def _query_opensky(lamin: float, lomin: float, lamax: float, lomax: float, access_token: Optional[str]=None):    
    url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def _query_opensky_flightinfo(icao24: str, access_token: Optional[str]=None):
    url = f"https://opensky-network.org/api/states/all?icao24={icao24}&time=0"
    # url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao24}&begin={int(time.time()-36000)}&end={int(time.time())}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()
        

def _extract_flights(data: dict, access_token: Optional[str]=None) -> List[FlightData]:
    flights = []

    states = data.get("states", [])
    if not states:
        return flights
    
    for state in states:
        state = dict(enumerate(state))
        icao24 = state.get(1, "").strip().lower()
        data = _query_opensky_flightinfo(icao24=icao24, access_token=access_token)
        
        velocity = state.get(9, "")
        latitude = state.get(6, "")
        longitude = state.get(5, "")
        geo_altitude = state.get(13, "")
        category = state.get(17, "")
        
        print(f"{icao24=}, {velocity=}, {latitude=}, {longitude=}, {geo_altitude=}, {category=}, {data=}")
        
        flights.append(
            FlightData(
                callsign=state.get(1, "").strip(),
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
    access_token = _auth_opensky()

    while True:
        try:
            data = _query_opensky(lamin=roi.lamin, lomin=roi.lomin, lamax=roi.lamax, lomax=roi.lomax, access_token=access_token)
            flights = _extract_flights(data, access_token=access_token)
            callback(flights)
        except Exception as e:
            print(f"[WARN] OpenSky query failed: {e}")

        time.sleep(update_interval)
