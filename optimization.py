import math

AIRCRAFT = {
    "A320": {"speed": 450, "fuel_factor": 2.6, "opt_alt": 37000},
    "B737": {"speed": 445, "fuel_factor": 2.7, "opt_alt": 36000},
}


def distance(route):
    return 300 + (len(route.split("-")) - 1) * 120


def fuel(distance, factor, wind, altitude, opt_alt):
    alt_eff = 1 - abs(altitude - opt_alt) / 100000
    wind_factor = 1 + (wind / 200)
    return distance * factor * wind_factor / alt_eff


def optimize_flight(flight, weather):
    perf = AIRCRAFT.get(flight["aircraft"], AIRCRAFT["A320"])

    dist = distance(flight["route"])
    base = fuel(dist, perf["fuel_factor"], weather["wind"], flight["altitude"], perf["opt_alt"])

    best_alt = flight["altitude"]
    best_fuel = base

    for alt in range(30000, 41000, 1000):
        f = fuel(dist, perf["fuel_factor"], weather["wind"], alt, perf["opt_alt"])
        if f < best_fuel:
            best_fuel = f
            best_alt = alt

    savings = base - best_fuel

    if weather["category"] in ["IFR", "LIFR"]:
        action = "Delay due to poor weather"
    elif weather["wind"] > 40:
        action = "Adjust route to avoid strong headwinds"
    else:
        action = f"Change altitude to {best_alt} ft"

    return {
        "original_fuel": round(base, 1),
        "optimized_fuel": round(best_fuel, 1),
        "savings_kg": round(savings, 1),
        "savings_pct": round((savings / base) * 100, 2),
        "recommended_action": action,
        "optimized_altitude": best_alt
    }