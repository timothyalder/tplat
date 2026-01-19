from skyscanner.roi import define_roi
from skyscanner.opensky import start_query_loop, FlightData


def flight_callback(flights: list[FlightData]) -> None:
    if not flights:
        print("No overhead flights.")
        return

    print(f"{len(flights)} overhead flight(s):")
    for f in flights:
        print(
            f"  Callsign: {f.callsign or 'N/A'} | "
            f"Origin: {f.origin or 'Unknown'} | "
            f"Destination: {f.destination or 'Unknown'}"
        )


def main():
    # Output from triangulate (example values)
    # Hawaii
    latitude = 21.388961
    longitude = -157.734384
    heading = 60.0  # degrees
    # Fadden
    latitude = -35.401512
    longitude = 149.114405
    heading = 150.0
    roi = define_roi(
        latitude=latitude,
        longitude=longitude,
        heading=heading,
        shape="rectangle",
    )
    start_query_loop(
        roi=roi,
        callback=flight_callback,
        update_interval=5,
    )


if __name__ == "__main__":
    main()
