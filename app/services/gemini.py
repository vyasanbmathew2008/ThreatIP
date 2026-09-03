import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)


async def analyze_traffic(ip_info: dict, behavior: dict, risk: dict) -> dict:
    prompt = f"""
Analyze this login-traffic telemetry for security triage.
Do not claim that an IP is definitely a human or bot. Use only observable evidence.
Return JSON only with keys: assessment, confidence, reason.

IP intelligence: {json.dumps(ip_info)}
Behavior: {json.dumps(behavior)}
Rule-based risk: {json.dumps(risk)}
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt,
    )

    text = response.text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"assessment": "unknown", "confidence": 0, "reason": text}
