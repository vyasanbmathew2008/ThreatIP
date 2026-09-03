from fastapi import FastAPI
from app.routes.security import router as security_router

app = FastAPI(
    title="ThreatIP",
    description="IP intelligence and risk scoring service for suspicious login traffic.",
    version="0.1.0",
)

app.include_router(security_router, prefix="/security", tags=["Security"])


@app.get("/")
async def root():
    return {"name": "ThreatIP", "status": "online"}
