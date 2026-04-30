import json
import requests
from metar.Metar import Metar
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-core")

METAR_URL = "https://aviationweather.gov/api/data/metar?ids={}&format=raw"
TAF_URL = "https://aviationweather.gov/api/data/taf?ids={}&format=raw"


def classify(obs):
    vis = obs.vis.value("SM") if obs.vis else 10
    if vis < 1: return "LIFR"
    if vis < 3: return "IFR"
    if vis < 5: return "MVFR"
    return "VFR"


@mcp.tool()
def get_weather_bundle(icao: str) -> str:
    metar_raw = requests.get(METAR_URL.format(icao)).text.strip()
    taf_raw = requests.get(TAF_URL.format(icao)).text.strip()

    obs = Metar(metar_raw)

    return json.dumps({
        "icao": icao,
        "metar": metar_raw,
        "taf": taf_raw,
        "wind": obs.wind_speed.value("KT") if obs.wind_speed else 0,
        "temp": obs.temp.value("C") if obs.temp else None,
        "category": classify(obs)
    }, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")