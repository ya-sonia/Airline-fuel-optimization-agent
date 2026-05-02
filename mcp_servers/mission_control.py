import json
import logging
import sys
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("mission_dispatch")

mcp = FastMCP("mission-dispatch")


@mcp.tool()
def dispatch_recommendation(payload: dict) -> str:
    """
    Send the final fuel optimization recommendation to mission control.

    Use this tool ONLY AFTER completing all analysis and generating
    the final recommendation.

    This simulates publishing the decision to airline operations.

    Required fields in payload:
    - flight_id: Flight identifier
    - origin: Departure airport
    - destination: Arrival airport
    - original_fuel: Fuel before optimization (kg)
    - optimized_fuel: Fuel after optimization (kg)
    - savings_kg: Fuel saved in kg
    - savings_pct: Percentage fuel savings
    - recommended_action: Final decision (e.g., altitude change)
    - rationale: Explanation of the decision

    Important:
    - Call this tool EXACTLY ONCE
    - This must be the FINAL step

    Returns:
        JSON with:
        - status: "sent" or "error"
        - payload: the dispatched recommendation
    """
    required = [
        "flight_id", "origin", "destination",
        "original_fuel", "optimized_fuel",
        "savings_kg", "savings_pct",
        "recommended_action", "rationale"
    ]

    missing = [k for k in required if k not in payload]
    if missing:
        return json.dumps({"status": "error", "missing": missing})

    payload["timestamp"] = datetime.now(timezone.utc).isoformat()

    logger.info(f"[MISSION] {payload['flight_id']} → {payload['recommended_action']}")

    return json.dumps({
        "status": "sent",
        "payload": payload
    }, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")