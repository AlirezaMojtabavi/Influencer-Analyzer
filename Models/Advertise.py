from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base
from datetime import datetime
import enum


class Advertise_Status(enum.Enum):
    Open = 'Open'
    Close = 'Close'


class Fraud_Analaysis(enum.Enum):
    Real = 'Real'
    Fake = 'Fake'


class Advertise(Base):
    __tablename__ = "advertises"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    mentioned_account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    mentioned_account = relationship("Account")

    influencer_id = Column(Integer, ForeignKey('influencers.id'))
    influencer = relationship('Influencer')

    start_date = Column(DateTime, default=datetime.now(), nullable=False)
    story_count = Column(Integer, default=1)
    follower_before_adv = Column(Integer, default=0)
    follower_after_1h = Column(Integer, default=0)
    follower_after_2h = Column(Integer, default=0)
    follower_after_12h = Column(Integer, default=0)
    follower_after_24h = Column(Integer, default=0)
    performance = Column(Integer, default=0)
    fraud_analaysis = Column(Enum(Fraud_Analaysis), default=Fraud_Analaysis.Real, nullable=False)
    status = Column(Enum(Advertise_Status), default=Advertise_Status.Open, nullable=False)

    def __init__(self, account_id, infl_id, start_date, follower_before):
        self.mentioned_account_id = account_id
        self.influencer_id = infl_id
        self.start_date = start_date
        self.follower_before_adv = follower_before

    def __str__(self):
        return self.mentioned_account.__str__()
