from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base
from datetime import datetime
import enum


class Monitoring_Status(enum.Enum):
    On = 'On'
    Off = 'Off'


class Influencer(Base):
    __tablename__ = "influencers"
    id = Column(Integer, primary_key=True, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="influencer")
    monitoring_start_date = Column(DateTime, default=datetime.now(), nullable=False)
    monitoring_finish_date = Column(DateTime, default=datetime.now(), nullable=False)
    monitoring_status = Column(Enum(Monitoring_Status), default=Monitoring_Status.Off, nullable=False)
    price = Column(Integer, nullable=True)

    def __init__(self, account, monitoring_start_date, monitoring_finish_date):
        self.account = account
        self.monitoring_start_date = monitoring_start_date
        self.monitoring_finish_date = monitoring_finish_date

    def __str__(self):
        return self.account.__str__()


