from Models.Account import Account
from Models.Influencer import Influencer, Monitoring_Status
from Models.Story import Story
from datetime import datetime, timedelta, timezone, time
from Database import session_scope
from sqlalchemy.orm import joinedload


class InfluencerRepository:
    def __init__(self):
        pass

    def Register_influencer(self, influencer_account, start_monitoring_Datetime, finish_monitoring_Datetime, price=None):
        with session_scope() as session:
            new_infl = Influencer(influencer_account, start_monitoring_Datetime, finish_monitoring_Datetime)
            if price is not None:
                new_infl.price = price
            session.flush()
            session.add(influencer_account)
            session.add(new_infl)
            session.commit()

    def check_influencer_exists(self, username):
        with session_scope() as session:
            infl_item = session.query(Influencer).join(Account).filter(Account.username == username).first()
            return infl_item.id if infl_item else None

    def update_inactive_influencers(self):
        with session_scope() as session:
            inactive_infls = session.query(Influencer).options(joinedload(Influencer.account)).filter(
                (Influencer.monitoring_start_date > datetime.now().astimezone(timezone.utc)) |
                (Influencer.monitoring_finish_date < datetime.now().astimezone(timezone.utc))
            ).all()

            for infl_item in inactive_infls:
                infl_item.monitoring_status = Monitoring_Status.Off
                setattr(infl_item, "monitoring_status", Monitoring_Status.Off)
            session.commit()

    def is_exist_story_id(self, infl_id, story_id):
        with session_scope() as session:
            story = session.query(Story).filter_by(story_id=story_id, influencer_id=infl_id).first()
            if story is not None:
                return True
            else:
                return False

    def register_story(self, infl_id, story_id, token_datetime):
        with session_scope() as session:
            new_story = Story(infl_id, story_id, token_datetime)
            session.flush()
            session.add(new_story)
            session.commit()

    def get_start_monitoring(self, infl_id):
        with session_scope() as session:
            infl_item = session.query(Influencer).filter(
                Influencer.id == infl_id).first()
            return infl_item.monitoring_start_date

    def get_all_influencers(self):
        with session_scope() as session:
            active_infls = session.query(Influencer).all()
            return [infl.id for infl in active_infls]

    def get_active_influencers(self):
        with session_scope() as session:
            active_infls = session.query(Influencer).filter(
                Influencer.monitoring_start_date <= datetime.now().astimezone(timezone.utc),
                Influencer.monitoring_finish_date >= datetime.now().astimezone(timezone.utc)).all()

            for infl_item in active_infls:
                infl_item.monitoring_status = Monitoring_Status.On
                setattr(infl_item, "monitoring_status", Monitoring_Status.On)
            session.commit()
            return [infl.id for infl in active_infls]

    def get_incomplete_infl(self):
        with session_scope() as session:
            infls = session.query(Influencer).join(Account).filter(
                (
                        Account.AVG_Like == 0.0 or
                        Account.engagement_rate == 0.0
                )
            ).all()
            return [infl.id for infl in infls]

    def update_statistical_properties(self, infl_id, like_average, comment_average, engagement_rate):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == infl_id).first()
            influencer.account.AVG_Like = like_average
            influencer.account.AVG_Comment = comment_average
            influencer.account.engagement_rate = engagement_rate
            setattr(influencer.account, "AVG_Like", like_average)
            setattr(influencer.account, "AVG_Comment", comment_average)
            setattr(influencer.account, "engagement_rate", engagement_rate)
            session.commit()

    def update_price(self, influencer_id, price):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == influencer_id).first()
            influencer.price = price
            setattr(influencer, "price", price)
            session.commit()


    def get_username(self, infl_id):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == infl_id).first()
            return influencer.account.username if influencer else None

    def get_user_id(self, infl_id):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == infl_id).first()
            return influencer.account.user_id if influencer else None

    def get_full_name(self, infl_id):
        with session_scope() as session:
            advert = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return advert.account.full_name if advert else None

    def get_bio(self, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.bio if infl else None

    def get_follower(self, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.follower if infl else None

    def get_media_count(self, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.Post if infl else None

    def get_AVG_Like(self, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.AVG_Like if infl else None

    def get_AVG_Comment(self, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.AVG_Comment if infl else None

    def get_engagement_rate(self, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.engagement_rate if infl else None

    def get_privacy(self, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.privacy if infl else None

    def set_monitoring_datetime(self, influencer_id, start_monitoring_Datetime, finish_monitoring_Datetime):
        with session_scope() as session:
            infl_item = session.query(Influencer).filter(Influencer.id == influencer_id).first()
            infl_item.monitoring_start_date = start_monitoring_Datetime
            infl_item.monitoring_finish_date = finish_monitoring_Datetime
            setattr(infl_item, "monitoring_start_date", start_monitoring_Datetime)
            setattr(infl_item, "monitoring_finish_date", finish_monitoring_Datetime)
            session.commit()

    def username_account_exists(self, acc_username):
        with session_scope() as session:
            acc_item = session.query(Account).filter(Account.username == acc_username).first()
            return acc_item if acc_item else None
