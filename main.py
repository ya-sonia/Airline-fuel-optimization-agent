import csv
import json
import re

from agent.agent import build_agent
from optimization import optimize_flight


def load_flights():
    flights = []
    with open("data/flights.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flights.append({
                "flight_id": row["flight_id"],
                "origin": row["origin"],
                "destination": row["destination"],
                "route": row["route"],
                "altitude": int(row["altitude"]),
                "aircraft": row["aircraft"]
            })
    return flights



def output(raw):
    text = str(raw)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    matches = re.findall(r"\{.*?\}", text, re.DOTALL)

    for m in matches[::-1]:  
        try:
            return json.loads(m)
        except:
            continue

    return {"error": "Invalid JSON", "raw": text}

def main():
    agent = build_agent()
    flights = load_flights()

    for flight in flights:
        print(f"\nProcessing {flight['flight_id']}...")

        # fallback weather
        weather = {"wind": 30, "category": "VFR"}

        local = optimize_flight(flight, weather)

        prompt = f"""
Flight:
{json.dumps(flight)}

Local Optimization:
{json.dumps(local)}

Use tools properly and finalize.
"""

        raw = agent(prompt)
        result = output(raw)

        if isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(result)


if __name__ == "__main__":
    main()
