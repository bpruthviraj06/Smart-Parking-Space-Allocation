from dataclasses import dataclass


@dataclass
class Vehicle:
    vehicle_number: str
    driver_name: str
    arrival_time: str
    departure_time: str
    status: str = "Parked"


def parse_time(t: str) -> int:
    """Convert 'HH:MM' to minutes since midnight."""
    h, m = map(int, t.split(":"))
    return h * 60 + m


def format_time(minutes: int) -> str:
    minutes %= 1440
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def run_sweep_line(vehicles: list[Vehicle]) -> dict:
    """
    Sweep-line algorithm: turn each vehicle into an arrival (+1) and
    departure (-1) event, sort chronologically (departures before arrivals
    on ties), and track the running count. The maximum running count is
    the minimum number of parking spaces required.
    """
    events = []
    for v in vehicles:
        if not v.arrival_time or not v.departure_time:
            continue
        events.append({"time": parse_time(v.arrival_time), "type": "arrival", "delta": 1, "vehicle": v})
        events.append({"time": parse_time(v.departure_time), "type": "departure", "delta": -1, "vehicle": v})

    # Sort by time; on a tie, departures before arrivals (frees a space first).
    events.sort(key=lambda e: (e["time"], 0 if e["type"] == "departure" else 1))

    current = 0
    peak = 0
    log = []
    for i, e in enumerate(events):
        current += e["delta"]
        peak = max(peak, current)
        log.append({
            "step": i + 1,
            "time": format_time(e["time"]),
            "type": e["type"],
            "delta": e["delta"],
            "vehicle": e["vehicle"].vehicle_number,
            "driver": e["vehicle"].driver_name,
            "current": current,
            "peak": peak,
        })

    return {"peak": peak, "log": log}


# --- Sample test data (6 overlapping intervals) ---
sample = [
    Vehicle("KA-01-AB-1234", "Aarav Sharma", "08:00", "11:30"),
    Vehicle("MH-02-CD-5678", "Diya Patel",   "09:15", "10:45"),
    Vehicle("DL-03-EF-9012", "Vikram Singh", "10:00", "13:00"),
    Vehicle("TN-04-GH-3456", "Meera Iyer",   "10:30", "12:15"),
    Vehicle("RJ-05-IJ-7890", "Rohan Nair",   "11:00", "14:30"),
    Vehicle("UP-06-KL-2345", "Sara Khan",    "12:00", "15:00"),
]

if __name__ == "__main__":
    result = run_sweep_line(sample)
    capacity = 3
    print(f"Total vehicles:        {len(sample)}")
    print(f"Peak concurrent (min spaces required): {result['peak']}")
    print(f"Capacity limit:         {capacity}")
    status = "Over Capacity" if result["peak"] > capacity else "Within Capacity"
    print(f"Capacity status:        {status}\n")
    print(f"{'#':>2}  {'Time':<5}  {'Type':<10}  {'Vehicle':<14}  {'Δ':>2}  {'Now':>3}  {'Peak':>4}")
    print("-" * 55)
    for entry in result["log"]:
        print(f"{entry['step']:>2}  {entry['time']:<5}  {entry['type']:<10}  "
              f"{entry['vehicle']:<14}  {entry['delta']:>+2}  {entry['current']:>3}  {entry['peak']:>4}")