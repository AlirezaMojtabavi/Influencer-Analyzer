from Models.Advertise import Advertise, AdvertiseStatus
from Models.Influencer import Influencer
from Database import session_scope
from datetime import datetime, timedelta, timezone


class AdvertiseRepository:
    @classmethod
    def register_advertise(cls, acc_id, influencer_id, start_datetime, followers_count):
        with session_scope() as session:
            new_adv = Advertise(acc_id, influencer_id, start_datetime, followers_count)
            session.add(new_adv)
            session.commit()

    @classmethod
    def check_advertise_exists(cls, infl_id, mentioned_id):
        with session_scope() as session:
            if mentioned_id is not None:
                adv_item = session.query(Advertise).filter(
                    Advertise.influencer_id == infl_id,
                    Advertise.status == AdvertiseStatus.Open,
                    Advertise.mentioned_account_id == mentioned_id
                ).first()
                return adv_item.id if adv_item else None
            else:
                return None

    @classmethod
    def plus_story_count(cls, adv_id_to_check):
        with session_scope() as session:
            advert = session.query(Advertise).filter(Advertise.id == adv_id_to_check).first()
            if advert:
                advert.story_count += 1
                setattr(advert, "story_count", advert.story_count)
                session.commit()

    @classmethod
    def get_all_infl_advs(cls, infl_id):
        with session_scope() as session:
            advert_ids = session.query(Advertise.id).join(Influencer).filter(
                Advertise.influencer_id == infl_id
            ).all()
            return [advert_id[0] for advert_id in advert_ids]

    @classmethod
    def get_active_influencer_advertises(cls, infl_id):
        with session_scope() as session:
            advert_ids = session.query(Advertise.id).join(Influencer).filter(
                Advertise.influencer_id == infl_id,
                Advertise.status == AdvertiseStatus.Open
            ).all()
            return [advert_id[0] for advert_id in advert_ids]

    @classmethod
    def get_start_datetime(cls, adv_id):
        with session_scope() as session:
            start_time = session.query(Advertise.start_date).filter(
                Advertise.id == adv_id
            ).first()

            return start_time[0].astimezone(timezone.utc)

    @classmethod
    def get_mentioned_username(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.username if advert else None

    @classmethod
    def get_mentioned_full_name(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.full_name if advert else None

    @classmethod
    def get_mentioned_bio(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.bio if advert else None

    @classmethod
    def get_follower_before(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_before_adv if advert else None

    @classmethod
    def get_mentioned_media_count(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.Post if advert else None

    @classmethod
    def get_mentioned_AVG_Like(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.AVG_Like if advert else None

    @classmethod
    def get_mentioned_AVG_Comment(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.AVG_Comment if advert else None

    @classmethod
    def get_mentioned_engagement_rate(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.engagement_rate if advert else None

    @classmethod
    def get_mentioned_privacy(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.privacy if advert else None

    @classmethod
    def get_mentioned_story_count(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.story_count if advert else None

    @classmethod
    def get_mentioned_status(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.api_status if advert else None

    @classmethod
    def set_follower_after_1h(cls, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_1h = followers_count
            setattr(advert, "follower_after_1h", followers_count)
            session.commit()

    @classmethod
    def set_follower_after_2h(cls, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_2h = followers_count
            setattr(advert, "follower_after_2h", followers_count)
            session.commit()

    @classmethod
    def set_follower_after_12h(cls, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_12h = followers_count
            setattr(advert, "follower_after_12h", followers_count)
            session.commit()

    @classmethod
    def set_follower_after_24h(cls, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_24h = followers_count
            setattr(advert, "follower_after_24h", followers_count)
            session.commit()

    @classmethod
    def get_follower_after_1h(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_1h

    @classmethod
    def get_follower_after_2h(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_2h

    @classmethod
    def get_follower_after_12h(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_12h

    @classmethod
    def get_follower_after_24h(cls, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_24h

    @classmethod
    def set_advertise_status(cls, adv_id, state):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.api_status = state
            setattr(advert, "status", state)
            session.commit()

    @classmethod
    def set_performance(cls, adv_id, performance):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.performance = performance
            setattr(advert, "performance", performance)
            session.commit()
