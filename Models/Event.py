from sqlalchemy import Column, Integer, String, Float, \
    Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .Base import Base
from datetime import datetime, timezone
import enum


class EventType(enum.Enum):
    Log = 'Log'
    Warning = 'Warning'
    Error = 'Error'


class EventCategory(enum.Enum):
    Authentication = 'Authentication'
    Reading_Media = 'Reading Media'
    Output_Generation = 'Output Generation'
    Cycle_Management = 'Cycle Management'


class EventName(enum.Enum):
    Login_Succeeded = 'Login Succeeded'
    Login_Failed = 'Login Failed'
    All_Changing_Account_Failed = 'All Changing Account Failed'
    Reading_Story = 'Reading Story'
    Reading_Follower_Count = 'Reading Follower Count'
    Reading_Post_Failed = 'Reading Post Failed'
    Reading_Profile_Failed = 'Reading Profile Failed'
    Reading_Story_Failed = 'Reading Story Failed'
    Update_Excel_Files = 'Update Excel Files'
    Update_Story_Table = 'Update Story Table'
    Cycle_Finished = 'Cycle Finished'
    Robot_Stopped = 'Robot Stopped'
    Reading_All_Story_Failed = 'Reading All Story Failed'


class RobotAPI(enum.Enum):
    Instagrapi = 'Instagrapi'
    Instaloader = 'Instaloader'


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(Enum(EventType), default=EventType.Log, nullable=False)
    category = Column(Enum(EventCategory), nullable=False)
    name = Column(Enum(EventName), nullable=False)
    occurrence_time = Column(DateTime, default=datetime.now(), nullable=False)
    occurrence_source = Column(String(60), nullable=False)
    robot_api = Column(Enum(RobotAPI), nullable=True)
    target_account = Column(String(30), nullable=True)
    bot_id = Column(Integer, ForeignKey('bots.id'), nullable=True)
    bot = relationship("Bot")
    content = Column(Text, nullable=True)

    def __init__(self, event_type, category, name, occurrence_source, robot_api=None,
                 target_account=None, bot_id=None, content=None):
        self.type = event_type
        self.category = category
        self.name = name
        self.occurrence_time = datetime.now(timezone.utc)
        self.occurrence_source = occurrence_source
        if robot_api and robot_api is not None:
            self.robot_api = robot_api
        if target_account and target_account is not None:
            self.target_account = target_account
        if bot_id and bot_id is not None:
            self.bot_id = bot_id
        if content and content is not None:
            self.content = content

    def __str__(self):
        return self.name
