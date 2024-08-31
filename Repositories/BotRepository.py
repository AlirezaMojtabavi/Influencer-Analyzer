from Models.Bot import Bot
from Database import session_scope
from sqlalchemy.orm import joinedload


class BotRepository:
    @classmethod
    def get_bot_id(cls, bot_username):
        with session_scope() as session:
            bot = session.query(Bot).filter(
                Bot.username == bot_username).first()
            return bot.id if bot else None
