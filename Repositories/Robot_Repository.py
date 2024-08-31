from Models.Event import Event
from Database import session_scope
from sqlalchemy.orm import joinedload


class EventRepository:
    @classmethod
    def register_event(cls, event_type, category, name, occurrence_source, robot_api=None,
                       target_account=None, bot_id=None, content=None):
        with session_scope() as session:
            new_event = Event(event_type=event_type, category=category, name=name, occurrence_source=occurrence_source,
                              robot_api=robot_api, target_account=target_account, bot_id=bot_id, content=content)
            session.flush()
            session.add(new_event)
            session.commit()
