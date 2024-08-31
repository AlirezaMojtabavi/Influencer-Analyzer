from Models.Advertise import Advertise, Advertise_Status
from Models.Account import Account
from Models.Influencer import Influencer
from Models.Story import Story
from Database import session_scope
from datetime import datetime, timedelta, timezone


class AdvertiseRepository:
    def __init__(self):
        pass

    def register_advertise(self, new_adv_acc, influencer_id, start_datetime, followers_count, repeated_acc_id=None):
        with session_scope() as session:
            if repeated_acc_id is None:
                # Add the new account and advertisement
                session.add(new_adv_acc)
                session.flush()
                # session.flush()
                new_adv = Advertise(new_adv_acc.id, influencer_id,
                                    start_datetime, followers_count)
                session.add(new_adv)
            else:
                # Fetch the account_item using account_item_id and attach it to the session
                account_item = session.query(Account).filter(Account.id == repeated_acc_id).first()
                if account_item:
                    # account_item.follower = followers_count
                    account_item = session.merge(account_item)
                    session.flush()
                    new_adv = Advertise(repeated_acc_id, influencer_id,
                                        start_datetime, followers_count)
                    # new_adv.mentioned_account_id = account_item.id
                    # session.flush()
                    session.add(new_adv)
            # Commit the transaction
            session.commit()

    def check_advertise_exists(self, infl_id, mentioned_id):
        with session_scope() as session:
            if mentioned_id is not None:
                adv_item = session.query(Advertise).filter(
                    Advertise.influencer_id == infl_id,
                    Advertise.status == Advertise_Status.Open,
                    Advertise.mentioned_account_id == mentioned_id
                ).first()
                return adv_item.id if adv_item else None
            else:
                return None

    def plus_story_count(self, adv_id_to_check):
        with session_scope() as session:
            advert = session.query(Advertise).filter(Advertise.id == adv_id_to_check).first()
            if advert:
                advert.story_count += 1
                setattr(advert, "story_count", advert.story_count)
                session.commit()

    def update_story_table(self):
        with session_scope() as session:
            now = datetime.now(timezone.utc)
            cutoff_time = now - timedelta(hours=24)
            story_items = session.query(Story).filter(Story.token_datetime < cutoff_time).all()
            for story in story_items:
                session.delete(story)
            session.commit()

    def check_account_exists(self, username):
        with session_scope() as session:
            account_item = session.query(Account).filter(
                Account.username == username
            ).first()
            return account_item.id if account_item else None


    def get_all_infl_advs(self, infl_id):
        with session_scope() as session:
            advert_ids = session.query(Advertise.id).join(Influencer).filter(
                Advertise.influencer_id == infl_id
            ).all()
            return [advert_id[0] for advert_id in advert_ids]


    def get_active_influencer_advertises(self, infl_id):
        with session_scope() as session:
            advert_ids = session.query(Advertise.id).join(Influencer).filter(
                Advertise.influencer_id == infl_id,
                Advertise.status == Advertise_Status.Open
            ).all()
            return [advert_id[0] for advert_id in advert_ids]

    def get_start_datetime(self, adv_id):
        with session_scope() as session:
            start_time = session.query(Advertise.start_date).filter(
                Advertise.id == adv_id
            ).first()

            return start_time[0].astimezone(timezone.utc)

    def get_mentioned_username(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.username if advert else None

    def get_mentioned_full_name(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.full_name if advert else None

    def get_mentioned_bio(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.bio if advert else None

    def get_follower_before(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_before_adv if advert else None

    def get_mentioned_media_count(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.Post if advert else None

    def get_mentioned_AVG_Like(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.AVG_Like if advert else None

    def get_mentioned_AVG_Comment(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.AVG_Comment if advert else None

    def get_mentioned_engagement_rate(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.engagement_rate if advert else None

    def get_mentioned_privacy(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.mentioned_account.privacy if advert else None

    def get_mentioned_story_count(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.story_count if advert else None

    def get_mentioned_status(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.status if advert else None

    def set_follower_after_1h(self, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_1h = followers_count
            setattr(advert, "follower_after_1h", followers_count)
            session.commit()

    def set_follower_after_2h(self, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_2h = followers_count
            setattr(advert, "follower_after_2h", followers_count)
            session.commit()

    def set_follower_after_12h(self, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_12h = followers_count
            setattr(advert, "follower_after_12h", followers_count)
            session.commit()

    def set_follower_after_24h(self, adv_id, followers_count):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.follower_after_24h = followers_count
            setattr(advert, "follower_after_24h", followers_count)
            session.commit()

    def get_follower_after_1h(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_1h

    def get_follower_after_2h(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_2h

    def get_follower_after_12h(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_12h

    def get_follower_after_24h(self, adv_id):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            return advert.follower_after_24h

    def set_advertise_status(self, adv_id, state):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.status = state
            setattr(advert, "status", state)
            session.commit()

    def set_performance(self, adv_id, performance):
        with session_scope() as session:
            advert = session.query(Advertise).filter(
                Advertise.id == adv_id
            ).first()
            advert.performance = performance
            setattr(advert, "performance", performance)
            session.commit()

