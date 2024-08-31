from sqlalchemy import Column, Integer, BigInteger, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from .Base import Base


class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, nullable=False)
    influencer_id = Column(Integer, ForeignKey('influencers.id'))
    influencer = relationship("Influencer")
    story_id = Column(String(50), nullable=False)
    token_datetime = Column(DateTime)

    def __init__(self, influencer_id, story_id, token_datetime):
        self.influencer_id = influencer_id
        self.story_id = story_id
        self.token_datetime = token_datetime

    def __str__(self):
        return self.story_id


