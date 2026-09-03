# ThreatIP

FastAPI-based IP intelligence and risk-scoring service for detecting suspicious login traffic and helping protect admin authentication systems.

## Features

- Automatic client IP detection from the backend request
- IP intelligence lookup
- Request-frequency tracking
- Failed-login behavior tracking
- Rule-based risk scoring
- Optional Gemini analysis for medium/high-risk traffic
- Allow, challenge, or block decisions
- Designed to run as a private internal security service

## Architecture

```text
Browser
   |
   v
Admin Login Backend
   |
   v
ThreatIP Security Service
   |---- IP Intelligence
   |---- Behavior Tracking
   |---- Risk Engine
   |---- Gemini (suspicious traffic only)
   |
   v
Allow / Challenge / Block
```

## Setup

```bash
git clone https://github.com/vyasanbmathew2008/ThreatIP.git
cd ThreatIP
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key
IP_API_URL=http://ip-api.com/json
```

Run:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The service is intended to be private. Do not expose the security endpoint directly to the public internet.

## Login Integration

The login backend should obtain the client IP from the server-side request and call ThreatIP **before validating username/password**.

```python
security_result = await check_security(ip)

if security_result["action"] == "block":
    return {"success": False, "message": "Access denied"}

if security_result["action"] == "challenge":
    return {"success": False, "challenge": True}

# Only now verify credentials.
```

Never send passwords, password hashes, session cookies, or authentication credentials to Gemini.

## Risk Model

The initial rule engine considers:

- Request frequency
- Failed login frequency
- Possible hosting/datacenter networks

Current actions:

- `0-49`: allow
- `50-79`: challenge
- `80-100`: block

These thresholds should be tuned for the application and stored in a shared production datastore such as Redis.

## Production Notes

ThreatIP is an application-layer login-abuse defense. It is **not a replacement for network-level DDoS protection**. For production deployments, place the application behind a CDN/WAF or other upstream DDoS mitigation service.

The current behavior store is in-memory for development. Use Redis for multi-worker or multi-server deployments.

IP intelligence should also be cached to reduce API usage and latency.

## Security

- Keep `.env` out of Git.
- Do not trust a browser-supplied IP query parameter for access control.
- Authenticate service-to-service requests when ThreatIP is deployed separately.
- Treat AI output as advisory rather than the sole security decision.
