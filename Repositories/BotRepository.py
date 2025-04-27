from Models.Bot import Bot, BotAccountStatus, LastLoginStatus
from Database import session_scope
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload


class BotRepository:
    @classmethod
    def get_bot_id(cls, bot_username):
        with session_scope() as session:
            bot = session.query(Bot).filter(
                Bot.username == bot_username).first()
            return bot.id if bot else None

    @classmethod
    def update_bot_authentication(cls, username, password, phone_number):
        with session_scope() as session:
            bot = session.query(Bot).filter(
                Bot.username == username).first()
            if bot is not None:
                bot.password = password
                bot.phone_number = phone_number
                setattr(bot, "password", password)
                setattr(bot, "phone_number", phone_number)
                session.commit()
            else:
                new_bot = Bot(username, password, phone_number)
                session.add(new_bot)
                session.commit()

    @classmethod
    def update_bot_content(cls, username, api_status, last_login_status=None, message=None):
        with session_scope() as session:
            bot = session.query(Bot).filter(
                Bot.username == username).first()
            if bot is not None:
                bot.account_status = api_status
                setattr(bot, "api_status", api_status)
                if not(api_status == BotAccountStatus.Standby):
                    bot.last_login_time = datetime.now(timezone.utc)
                    setattr(bot, "last_login_time", datetime.now(timezone.utc))
                if last_login_status and last_login_status is not None:
                    bot.last_login_status = last_login_status
                    setattr(bot, "last_login_status", last_login_status)
                if message and message is not None:
                    bot.last_error_message = message
                    setattr(bot, "last_error_message", message)
                session.commit()

    @classmethod
    def update_inactive_bots(cls, bots_account_array):
        account_usernames = [item[1] for item in bots_account_array]
        with session_scope() as session:
            missing_bots = session.query(Bot).where(~Bot.username.in_(account_usernames)).all()
            for bot in missing_bots:
                bot.account_status = BotAccountStatus.Off
                setattr(bot, "account_status", BotAccountStatus.Off)
            session.commit()

