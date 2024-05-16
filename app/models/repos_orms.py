"""
数据表映射
"""
from sqlalchemy import Column, Float, Integer, String

from app.utils.database import Base


class Properties(Base):
    __tablename__ = 'properties'
    __table_args__ = {'schema': 'HOUSE'}

    Id = Column(String, primary_key=True)  # 配方单主键
    Community = Column(Integer, nullable=True)
    ApartmentLayout = Column(Integer, nullable=True)
    Area = Column(Integer, nullable=True)
    Floor = Column(Integer, nullable=True)
    ConstructionYear = Column(Integer, nullable=True)
    TotalPrice = Column(Integer, nullable=True)
    UnitPrice = Column(Integer, nullable=True)
    Orientation = Column(Integer, nullable=True)
    RenovationDegree = Column(Integer, nullable=True)
    Elevator = Column(Integer, nullable=True)
    PlotRatio = Column(Float, nullable=True)
    GreeneryRate = Column(Float, nullable=True)
    PropertyFee = Column(Float, nullable=True)
    DistanceToWasteStation_km = Column(Float, nullable=True)
    SurroundingBusLines_05km = Column(Integer, nullable=True)
    SurroundingSchools_1km = Column(Integer, nullable=True)
    DistanceToSubway_km = Column(Float, nullable=True)
    DistanceToBusinessDistrict_km = Column(Integer, nullable=True)
    DistanceToPark_km = Column(Float, nullable=True)
    AgentSafetyScore = Column(Float, nullable=True)
    AgentComfortScore = Column(Integer, nullable=True)
    AgentValueForMoneyScore = Column(Float, nullable=True)
    AgentLocationScore = Column(Integer, nullable=True)
    AgentFutureAppreciationScore = Column(Integer, nullable=True)
    AgentEnvironmentalScore = Column(Integer, nullable=True)
    AgentPropertyServiceScore = Column(Float, nullable=True)
