from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SpeedTestCreate(BaseModel):
    test_id: str
    ip_address: str
    isp: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latency_min: Optional[float] = None
    latency_avg: Optional[float] = None
    latency_max: Optional[float] = None
    jitter: Optional[float] = None
    download_mbps: Optional[float] = None
    upload_mbps: Optional[float] = None
    user_agent: Optional[str] = None


class SpeedTestResponse(SpeedTestCreate):
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
