import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

load_dotenv()

BASE = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT = """
You are an Airline Fuel Optimization AI.

STRICT RULES:
- Return ONLY ONE JSON
- DO NOT repeat output
- DO NOT explain anything
- STOP after final answer

TOOL USAGE (VERY STRICT):
- Call get_weather_bundle EXACTLY ONCE for origin
- Call get_weather_bundle EXACTLY ONCE for destination
- NEVER call same tool multiple times
- Call dispatch_recommendation EXACTLY ONCE at the end

LOGIC:
- Use local optimization as base
- Adjust using:
    • altitude efficiency
    • wind impact
    • safety (IFR/LIFR)

RATIONALE MUST include at least one:
- altitude efficiency OR
- wind impact OR
- safety reasoning

OUTPUT FORMAT:

{
  "flight_id": "...",
  "origin": "...",
  "destination": "...",
  "original_fuel": number,
  "optimized_fuel": number,
  "savings_kg": number,
  "savings_pct": number,
  "recommended_action": "...",
  "rationale": "...",
  "mission_control_status": "sent"
}

IMPORTANT:
- After generating JSON → STOP
- DO NOT repeat JSON
"""


def build_agent():
    model = OllamaModel(
        host=os.getenv("HOST"),
        model_id=os.getenv("MODEL_ID")
    )

    weather = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command=sys.executable,
            args=[str(BASE / "mcp_servers/weather_server.py")]
        )
    ))

    mission = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command=sys.executable,
            args=[str(BASE / "mcp_servers/mission_control.py")]
        )
    ))

    weather.start()
    mission.start()

    tools = weather.list_tools_sync() + mission.list_tools_sync()

    return Agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )



