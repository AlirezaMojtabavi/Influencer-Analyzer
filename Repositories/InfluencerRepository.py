from Models.Account import Account, Privacy
from Models.Influencer import Influencer, MonitoringStatus
from Models.Story import Story
from datetime import datetime, timedelta, timezone, time
from Database import session_scope
from sqlalchemy.orm import joinedload


class InfluencerRepository:
    @classmethod
    def register_influencer(cls, account_id, start_monitoring_datetime, finish_monitoring_datetime,
                            price=None):
        with session_scope() as session:
            new_infl = Influencer(account_id, start_monitoring_datetime, finish_monitoring_datetime)
            if price is not None:
                new_infl.price = price
            session.add(new_infl)
            session.commit()

    @classmethod
    def check_influencer_exists(cls, username):
        with session_scope() as session:
            infl_item = session.query(Influencer).join(Account).filter(Account.username == username).first()
            return infl_item.id if infl_item else None

    @classmethod
    def update_inactive_influencers(cls):
        with session_scope() as session:
            inactive_infls = session.query(Influencer).options(joinedload(Influencer.account)).filter(
                (Influencer.monitoring_start_date > datetime.now().astimezone(timezone.utc)) |
                (Influencer.monitoring_finish_date < datetime.now().astimezone(timezone.utc))
            ).all()

            for infl_item in inactive_infls:
                infl_item.monitoring_status = MonitoringStatus.Off
                setattr(infl_item, "monitoring_status", MonitoringStatus.Off)
            session.commit()

    @classmethod
    def is_exist_story_id(cls, infl_id, story_id):
        with session_scope() as session:
            story = session.query(Story).filter_by(story_id=story_id, influencer_id=infl_id).first()
            if story is not None:
                return True
            else:
                return False

    @classmethod
    def register_story(cls, infl_id, story_id, token_datetime):
        with session_scope() as session:
            new_story = Story(infl_id, story_id, token_datetime)
            session.flush()
            session.add(new_story)
            session.commit()

    @classmethod
    def update_story_table(cls):
        with session_scope() as session:
            now = datetime.now(timezone.utc)
            cutoff_time = now - timedelta(hours=24)
            story_items = session.query(Story).filter(Story.token_datetime < cutoff_time).all()
            for story in story_items:
                session.delete(story)
            session.commit()

    @classmethod
    def get_start_monitoring(cls, infl_id):
        with session_scope() as session:
            infl_item = session.query(Influencer).filter(
                Influencer.id == infl_id).first()
            return infl_item.monitoring_start_date

    @classmethod
    def get_all_infl_ids(cls):
        with session_scope() as session:
            active_infls = session.query(Influencer).all()
            return [infl.id for infl in active_infls]

    @classmethod
    def get_all_infls_acc_id(cls):
        with session_scope() as session:
            active_infls = session.query(Influencer).all()
            return [infl.account_id for infl in active_infls]

    @classmethod
    def get_active_influencers(cls):
        with session_scope() as session:
            active_infls = session.query(Influencer).filter(
                Influencer.monitoring_start_date <= datetime.now().astimezone(timezone.utc),
                Influencer.monitoring_finish_date >= datetime.now().astimezone(timezone.utc)).all()

            for infl_item in active_infls:
                infl_item.monitoring_status = MonitoringStatus.On
                setattr(infl_item, "monitoring_status", MonitoringStatus.On)
            session.commit()
            return [infl.id for infl in active_infls]

    @classmethod
    def get_incomplete_infl(cls):
        with session_scope() as session:
            infls = session.query(Influencer).join(Account).filter(
                (
                        Account.AVG_Like == 0.0 or
                        Account.engagement_rate == 0.0
                )
            ).all()
            return [infl.id for infl in infls]

    @classmethod
    def update_statistical_properties(cls, infl_id, like_average, comment_average, engagement_rate):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == infl_id).first()
            influencer.account.AVG_Like = like_average
            influencer.account.AVG_Comment = comment_average
            influencer.account.engagement_rate = engagement_rate
            setattr(influencer.account, "AVG_Like", like_average)
            setattr(influencer.account, "AVG_Comment", comment_average)
            setattr(influencer.account, "engagement_rate", engagement_rate)
            session.commit()

    @classmethod
    def update_price(cls, influencer_id, price):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == influencer_id).first()
            influencer.price = price
            setattr(influencer, "price", price)
            session.commit()

    @classmethod
    def get_username(cls, infl_id):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == infl_id).first()
            return influencer.account.username if influencer else None

    @classmethod
    def get_user_id(cls, infl_id):
        with session_scope() as session:
            influencer = session.query(Influencer).filter(Influencer.id == infl_id).first()
            return influencer.account.user_id if influencer else None

    @classmethod
    def get_full_name(cls, infl_id):
        with session_scope() as session:
            advert = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return advert.account.full_name if advert else None

    @classmethod
    def get_bio(cls, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.bio if infl else None

    @classmethod
    def get_follower(cls, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.follower if infl else None

    @classmethod
    def get_media_count(cls, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.Post if infl else None

    @classmethod
    def get_AVG_Like(cls, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.AVG_Like if infl else None

    @classmethod
    def get_AVG_Comment(cls, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.AVG_Comment if infl else None

    @classmethod
    def get_engagement_rate(cls, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.engagement_rate if infl else None

    @classmethod
    def get_privacy(cls, infl_id):
        with session_scope() as session:
            infl = session.query(Influencer).filter(
                Influencer.id == infl_id
            ).first()
            return infl.account.privacy if infl else None

    @classmethod
    def set_monitoring_datetime(cls, influencer_id, start_monitoring_Datetime, finish_monitoring_Datetime):
        with session_scope() as session:
            infl_item = session.query(Influencer).filter(Influencer.id == influencer_id).first()
            infl_item.monitoring_start_date = start_monitoring_Datetime
            infl_item.monitoring_finish_date = finish_monitoring_Datetime
            setattr(infl_item, "monitoring_start_date", start_monitoring_Datetime)
            setattr(infl_item, "monitoring_finish_date", finish_monitoring_Datetime)
            session.commit()


