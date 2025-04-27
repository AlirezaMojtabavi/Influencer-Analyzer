from Repositories.AdvertiseRepository import AdvertiseRepository as AdvRepo, AdvertiseStatus
from datetime import datetime, timezone
from Repositories.EventRepository import EventRepository, EventCategory, EventType, EventName, RobotAPI
from Repositories.AccountRepository import AccountRepository as AccRepo, Privacy


class AdvertiseManager:
    def __init__(self, acc_manager):
        self.acc_manager = acc_manager

    def create_advertise(self, acc_username, infl_id, start_datetime):
        acc_id_check = AccRepo.check_account_exists(acc_username)
        acc_profile, acc_user_id, followers_count, acc_media_count = \
            self.acc_manager.read_account_profile(acc_username)
        if acc_id_check is None:
            acc_fullname = acc_profile.full_name[:100]
            acc_bio = acc_profile.biography[:200]
            acc_privacy = Privacy.Private if acc_profile.is_private else Privacy.Public
            like_avrg, comment_avrg, engagement = self.acc_manager.calculate_statistical_properties(acc_user_id,
                                                                                                    followers_count,
                                                                                                    acc_username)

            if like_avrg:
                new_adv_acc_id = self.acc_manager.create_account(acc_username, acc_user_id, acc_fullname,
                                                                 acc_bio, followers_count, acc_media_count,
                                                                 like_avrg, comment_avrg, engagement, acc_privacy)

            else:
                new_adv_acc_id = self.acc_manager.create_account(acc_username, acc_user_id, acc_fullname,
                                                                 acc_bio, followers_count, acc_media_count, 0,
                                                                 0, 0, acc_privacy)

            AdvRepo.register_advertise(new_adv_acc_id, infl_id, start_datetime, followers_count)
        else:
            AdvRepo.register_advertise(acc_id_check, infl_id, start_datetime, followers_count)

    def get_active_influencer_advertises(self, infl_id):
        return AdvRepo.get_active_influencer_advertises(infl_id)

    def get_delta_time(self, adv_id):
        current_delta_time = datetime.now().astimezone(timezone.utc) - \
                             AdvRepo.get_start_datetime(adv_id)
        mentioned_username = AdvRepo.get_mentioned_username(adv_id)

        return current_delta_time, mentioned_username

    def set_follower_after_1h(self, adv_id, followers_count):
        AdvRepo.set_follower_after_1h(adv_id, followers_count)

    def set_follower_after_2h(self, adv_id, followers_count):
        AdvRepo.set_follower_after_2h(adv_id, followers_count)

    def set_follower_after_12h(self, adv_id, followers_count):
        AdvRepo.set_follower_after_12h(adv_id, followers_count)

    def set_follower_after_24h(self, adv_id, followers_count):
        AdvRepo.set_follower_after_24h(adv_id, followers_count)
        performance = followers_count - AdvRepo.get_follower_before(adv_id)
        AdvRepo.set_performance(adv_id, performance)

    def get_follower_after_1h(self, adv_id):
        return AdvRepo.get_follower_after_1h(adv_id)

    def get_follower_after_2h(self, adv_id):
        return AdvRepo.get_follower_after_2h(adv_id)

    def get_follower_after_12h(self, adv_id):
        return AdvRepo.get_follower_after_12h(adv_id)

    def get_follower_after_24h(self, adv_id):
        return AdvRepo.get_follower_after_24h(adv_id)

    def set_advertise_status(self, adv_id, status):
        AdvRepo.set_advertise_status(adv_id, status)
