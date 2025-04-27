from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base
from datetime import datetime
import enum


class MonitoringStatus(enum.Enum):
    On = 'On'
    Off = 'Off'


class Influencer(Base):
    __tablename__ = "influencers"
    id = Column(Integer, primary_key=True, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="influencer")
    monitoring_start_date = Column(DateTime, default=datetime.now(), nullable=False)
    monitoring_finish_date = Column(DateTime, default=datetime.now(), nullable=False)
    monitoring_status = Column(Enum(MonitoringStatus), default=MonitoringStatus.Off, nullable=False)
    price = Column(Integer, nullable=True)

    def __init__(self, account_id, monitoring_start_date, monitoring_finish_date):
        self.account_id = account_id
        self.monitoring_start_date = monitoring_start_date
        self.monitoring_finish_date = monitoring_finish_date

    def __str__(self):
        return self.account.__str__()


