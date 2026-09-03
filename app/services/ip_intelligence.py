import httpx
from app.config import settings


async def get_ip_information(ip: str) -> dict:
    fields = (
        "status,message,country,countryCode,region,regionName,"
        "city,zip,lat,lon,timezone,isp,org,as,query"
    )
    url = f"{settings.ip_api_url}/{ip}"

    async with httpx.AsyncClient(timeout=3.0) as client:
        response = await client.get(url, params={"fields": fields})

    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError(data.get("message", "IP lookup failed"))

    return data
