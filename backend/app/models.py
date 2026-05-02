from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.sql import func
from .database import Base


class SpeedTest(Base):
    __tablename__ = "speed_tests"

    test_id     = Column(String(36), primary_key=True, index=True)
    ip_address  = Column(String(45), nullable=False)
    isp         = Column(String(255), nullable=True)
    city        = Column(String(100), nullable=True)
    country     = Column(String(100), nullable=True)
    latency_min = Column(Float, nullable=True)
    latency_avg = Column(Float, nullable=True)
    latency_max = Column(Float, nullable=True)
    jitter      = Column(Float, nullable=True)
    download_mbps = Column(Float, nullable=True)
    upload_mbps   = Column(Float, nullable=True)
    user_agent  = Column(Text, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
