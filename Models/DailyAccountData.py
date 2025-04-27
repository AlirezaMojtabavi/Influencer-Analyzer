from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .Base import Base
from Models.Influencer import MonitoringStatus
from Models.Account import Privacy


class DailyAccountData(Base):
    __tablename__ = 'dailyAccountData'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now(), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account")
    follower_count = Column(Integer, nullable=False)
    AVG_Like = Column(Float, default=0.0)
    AVG_Comment = Column(Float, default=0.0)
    AVG_share = Column(Integer)
    AVG_save = Column(Integer)
    engagement_rate = Column(Float, default=0.0)
    post_count = Column(Integer)
    story_count = Column(Integer)
    monitoring_status = Column(Enum(MonitoringStatus), default=MonitoringStatus.Off, nullable=False)
    privacy = Column(Enum(Privacy), default=Privacy.Public, nullable=False)
    price = Column(Integer, nullable=True)

    def __init__(self, account_id, follower, AVG_Like, AVG_Comment, AVG_share, AVG_save,
                 engagement_rate, stories, posts, monitoring_status, privacy, price):
        self.time = datetime.now(timezone.utc)
        self.account_id = account_id
        self.follower_count = follower
        self.AVG_Like = AVG_Like
        self.AVG_Comment = AVG_Comment
        self.AVG_share = AVG_share
        self.AVG_save = AVG_save
        self.engagement_rate = engagement_rate
        self.story_count = stories
        self.Post = posts
        self.monitoring_status = monitoring_status
        self.privacy = privacy
        self.price = price

    def __str__(self):
        return self.account.__str__()
