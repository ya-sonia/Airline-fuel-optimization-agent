import csv
import json
import re

from agent.agent import build_agent
from optimization import optimize_flight

from rich.table import Table
from rich.console import Console

console = Console()



# LOAD FLIGHTS FROM CSV

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

    # extract JSON objects
    matches = re.findall(r"\{.*?\}", text, re.DOTALL)

    for m in matches[::-1]:  # take last valid JSON
        try:
            return json.loads(m)
        except:
            continue

    return {"error": "Invalid JSON", "raw": text}



def run_pipeline(flights):
    agent = build_agent()
    results = []

    for flight in flights:
        print(f"\nProcessing {flight['flight_id']}...")

        
        weather = {"wind": 30, "category": "VFR"}

        # local optimization
        local = optimize_flight(flight, weather)

        # prompt to LLM agent
        prompt = f"""
Flight:
{json.dumps(flight)}

Local Optimization:
{json.dumps(local)}

IMPORTANT:
- Include rationale with altitude efficiency OR wind impact OR safety
- Always return valid JSON

Finalize using tools.
"""

        raw = agent(prompt)
        result = output(raw)

        
        if "error" in result:
            result = {
                "flight_id": flight["flight_id"],
                "origin": flight["origin"],
                "destination": flight["destination"],
                **local,
                "rationale": "Fallback: Based on local optimization only",
                "mission_control_status": "fallback"
            }

        results.append(result)

    return results



def print_summary_table(results):
    table = Table(title=" Airline Fuel Optimization Summary")

    table.add_column("Flight", style="cyan")
    table.add_column("Route")
    table.add_column("Fuel Before")
    table.add_column("Fuel After")
    table.add_column("Savings %")
    table.add_column("Action")

    for r in results:
        table.add_row(
            r["flight_id"],
            f"{r['origin']}→{r['destination']}",
            str(r["original_fuel"]),
            str(r["optimized_fuel"]),
            str(r["savings_pct"]),
            r["recommended_action"]
        )

    console.print(table)



def main():
    flights = load_flights()

    results = run_pipeline(flights)

    print("\n FINAL RESULTS:\n")
    for r in results:
        print(json.dumps(r, indent=2))

    print_summary_table(results)


if __name__ == "__main__":
    main()