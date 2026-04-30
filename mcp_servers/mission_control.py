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