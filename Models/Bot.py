from sqlalchemy import Column, Integer, String, Float, Enum,\
    DateTime, Text
from .Base import Base
from datetime import datetime
import enum


class BotAccountStatus(enum.Enum):
    InstaGrapi = 'InstaGrapi'
    Instaloader = 'Instaloader'
    Standby = 'Standby'
    Off = 'Off'


class LastLoginStatus(enum.Enum):
    Successful = 'Successful'
    Failed = 'Failed'
    Unused = 'Unused'


class Bot(Base):
    __tablename__ = "bots"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(40), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=False)
    account_status = Column(Enum(BotAccountStatus), default=BotAccountStatus.Standby, nullable=False)
    last_login_status = Column(Enum(LastLoginStatus), default=LastLoginStatus.Unused)
    last_login_time = Column(DateTime, nullable=True)
    last_error_message = Column(Text, nullable=True)

    def __init__(self, username, password, phone_number):
        self.username = username
        self.password = password
        self.phone_number = phone_number

    def __str__(self):
        return self.username
