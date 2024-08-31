from sqlalchemy import Column, Integer, String, Float, Enum, BigInteger
from sqlalchemy.orm import relationship
from .Base import Base
import enum


class Privacy(enum.Enum):
    Public = 'Public'
    Private = 'Private'


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String(35), unique=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    full_name = Column(String(100), nullable=False)
    bio = Column(String(200), nullable=False)
    follower = Column(Integer, nullable=False)
    Post = Column(Integer)
    AVG_Like = Column(Float, default=0.0)
    AVG_Comment = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    privacy = Column(Enum(Privacy), default=Privacy.Public, nullable=False)
    content_type = Column(String(50), nullable=True)

    influencer = relationship("Influencer", back_populates="account", uselist=False)

    def __init__(self, username, user_id, full_name, bio, follower, Post, AVG_Like, AVG_Comment,
                 engagement_rate, privacy):
        self.username = username
        self.user_id = user_id
        self.full_name = full_name
        self.bio = bio
        self.follower = follower
        self.Post = Post
        self.AVG_Like = AVG_Like
        self.AVG_Comment = AVG_Comment
        self.engagement_rate = engagement_rate
        self.privacy = privacy

    def __str__(self):
        return self.username
