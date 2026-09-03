from fastapi import APIRouter, Request, HTTPException

from app.services.gemini import analyze_traffic
from app.services.ip_intelligence import get_ip_information
from app.services.risk_engine import calculate_risk
from app.storage.memory import get_behavior, record_request

router = APIRouter()


@router.get("/check")
async def check_security(request: Request):
    ip = request.client.host if request.client else None
    if not ip:
        raise HTTPException(status_code=400, detail="Unable to determine client IP")

    record_request(ip)
    behavior = get_behavior(ip)

    try:
        ip_info = await get_ip_information(ip)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"IP intelligence lookup failed: {exc}")

    risk = calculate_risk(ip_info, behavior)
    ai_analysis = None

    if risk["level"] in {"medium", "high"}:
        try:
            ai_analysis = await analyze_traffic(ip_info, behavior, risk)
        except Exception as exc:
            ai_analysis = {"assessment": "unavailable", "reason": str(exc)}

    return {
        "ip": ip,
        "ip_info": ip_info,
        "behavior": behavior,
        "risk": risk,
        "ai_analysis": ai_analysis,
    }
