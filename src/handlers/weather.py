import json
import os
import traceback
from typing import Any, Dict

import requests
from requests.exceptions import HTTPError, RequestException

API_URL = "https://api.api-ninjas.com/v1/weather"
API_KEY = os.environ.get("API_NINJAS_KEY", "f/Lbqc8xujCtqRs8bZgXlA==xWx0MnDFYDiRDCo7")


def build_mcp_envelope(status: str, payload: Any, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {"status": status, "metadata": metadata or {}, "payload": payload}


def fetch_weather_for_coords(lat: float, lon: float) -> Dict[str, Any]:
    resp = requests.get(API_URL, headers={"X-Api-Key": API_KEY}, params={"lat": lat, "lon": lon}, timeout=6)
    resp.raise_for_status()
    return resp.json()


def weather(event, context=None):
    try:
        # Read lat/lon only from JSON body
        body = event.get("body")
        if not body:
            return {"statusCode": 400, "body": json.dumps(build_mcp_envelope("error", {"message": "JSON body with lat and lon is required"}))}

        try:
            parsed = json.loads(body)
        except Exception:
            return {"statusCode": 400, "body": json.dumps(build_mcp_envelope("error", {"message": "Invalid JSON body"}))}

        lat = parsed.get("lat")
        lon = parsed.get("lon")

        if lat is None or lon is None:
            return {"statusCode": 400, "body": json.dumps(build_mcp_envelope("error", {"message": "lat and lon are required in the JSON body"}))}

        try:
            lat = float(lat)
            lon = float(lon)
        except Exception:
            return {"statusCode": 400, "body": json.dumps(build_mcp_envelope("error", {"message": "lat and lon must be numbers"}))}

        data = fetch_weather_for_coords(lat, lon)
        envelope = build_mcp_envelope("ok", data, metadata={"source": "api-ninjas", "lat": lat, "lon": lon})
        return {"statusCode": 200, "body": json.dumps(envelope)}

    except HTTPError as he:
        tb = traceback.format_exc()
        code = he.response.status_code if getattr(he, "response", None) is not None else 502
        return {"statusCode": code, "body": json.dumps(build_mcp_envelope("error", {"message": str(he), "trace": tb}))}
    except RequestException as re:
        tb = traceback.format_exc()
        return {"statusCode": 502, "body": json.dumps(build_mcp_envelope("error", {"message": str(re), "trace": tb}))}
    except Exception as e:
        tb = traceback.format_exc()
        return {"statusCode": 500, "body": json.dumps(build_mcp_envelope("error", {"message": str(e), "trace": tb}))}
