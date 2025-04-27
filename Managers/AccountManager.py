from Repositories.AccountRepository import AccountRepository as AccRepo, Privacy
from Repositories.InfluencerRepository import InfluencerRepository as InflRepo
from datetime import datetime, timezone, timedelta
import random
from time import sleep
from Repositories.EventRepository import EventRepository, EventCategory, EventType, EventName, RobotAPI


class AccountManager:
    def __init__(self, bot):
        self.IA_engine = bot

    def create_account(self, acc_username, acc_user_id, full_name, biography, followers_count,
                       media_count, like_average, comment_average, activity_per_follower,
                       influencer_privacy):
        if not like_average:
            new_acc_id = AccRepo.register_account(acc_username, acc_user_id, full_name, biography,
                                                  followers_count, media_count, 0,
                                                  0, 0, influencer_privacy)
        else:
            new_acc_id = AccRepo.register_account(acc_username, acc_user_id, full_name, biography,
                                                  followers_count, media_count, like_average, comment_average,
                                                  activity_per_follower, influencer_privacy)
        return new_acc_id

    def read_account_profile(self, account_username, account_user_id=None):
        try:
            acc_profile = self.IA_engine.loader_engine.check_profile_id(account_username)
            acc_user_id = acc_profile.userid
            followers_count = acc_profile.followers
            media_count = acc_profile.mediacount
            return acc_profile, acc_user_id, followers_count, media_count
        except Exception as e:
            EventRepository.register_event(EventType.Error, EventCategory.Reading_Media,
                                           EventName.Reading_Profile_Failed,
                                           "AccountManager::read_account_profile",
                                           robot_api=RobotAPI.Instaloader, target_account=account_username,
                                           bot_id=self.IA_engine.get_loader_acc_id(), content=str(e))
            login_flag = self.IA_engine.change_account("Loader")
            if login_flag:
                try:
                    acc_profile = self.IA_engine.loader_engine.check_profile_id(account_username)
                    acc_user_id = acc_profile.userid
                    followers_count = acc_profile.followers
                    media_count = acc_profile.mediacount
                    return acc_profile, acc_user_id, followers_count, media_count
                except Exception as e:
                    EventRepository.register_event(EventType.Error, EventCategory.Reading_Media,
                                                   EventName.Reading_Profile_Failed,
                                                   "AccountManager::read_account_profile",
                                                   robot_api=RobotAPI.Instaloader,
                                                   bot_id=self.IA_engine.get_loader_acc_id(),
                                                   target_account=account_username,
                                                   content=str(e))
                    try:
                        if account_user_id and account_user_id is not None:
                            acc_profile = self.IA_engine.grapi_engine.user_info(account_user_id)
                            acc_user_id = account_user_id
                        else:
                            acc_user_id = self.IA_engine.grapi_engine.user_id_from_username(account_username)
                            acc_profile = self.IA_engine.grapi_engine.user_info(acc_user_id)

                        followers_count = acc_profile.follower_count
                        media_count = acc_profile.media_count
                        return acc_profile, acc_user_id, followers_count, media_count
                    except Exception as e:
                        EventRepository.register_event(EventType.Error, EventCategory.Reading_Media,
                                                       EventName.Reading_Profile_Failed,
                                                       "AccountManager::read_account_profile",
                                                       robot_api=RobotAPI.Instagrapi,
                                                       bot_id=self.IA_engine.get_grapi_acc_id(),
                                                       target_account=account_username,
                                                       content=str(e))
                        return False, False, False, False
            else:
                EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                               EventName.All_Changing_Account_Failed,
                                               "AccountManager::read_account_profile",
                                               robot_api=RobotAPI.Instaloader, target_account=account_username,
                                               bot_id=self.IA_engine.get_loader_acc_id())
                return False, False, False, False

    def calculate_statistical_properties(self, user_id, followers_count, username):
        SINCE = datetime.now().date()
        UNTIL = SINCE - timedelta(days=300)
        try:
            posts = self.IA_engine.grapi_engine.user_medias(user_id, 50)
        except Exception as e:
            EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                           EventName.Reading_Post_Failed, "AccountManager::calculate_statistical",
                                           robot_api=RobotAPI.Instagrapi, target_account=username,
                                           bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))

            self.IA_engine.grapi_engine.logger.exception(e)
            sleep(random.randint(10, 20))
            relogin_flag = self.IA_engine.relogin_grapi("AccountManager::calculate_statistical",
                                                        username)
            if relogin_flag:
                try:
                    posts = self.IA_engine.grapi_engine.user_medias(user_id, 50)
                except Exception as e:
                    EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                   EventName.Reading_Post_Failed,
                                                   "AccountManager::calculate_statistical",
                                                   robot_api=RobotAPI.Instagrapi, target_account=username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                    login_flag = self.IA_engine.change_account()
                    if login_flag:
                        try:
                            posts = self.IA_engine.grapi_engine.user_medias(user_id, 50)
                        except Exception as e:
                            EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                           EventName.Reading_Post_Failed,
                                                           "AccountManager::calculate_statistical",
                                                           robot_api=RobotAPI.Instagrapi, target_account=username,
                                                           bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                            return False, False, False, False
                    else:
                        EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                                       EventName.All_Changing_Account_Failed,
                                                       "AccountManager::calculate_statistical",
                                                       robot_api=RobotAPI.Instagrapi, target_account=username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id())
                        return False, False, False, False
            else:
                login_flag = self.IA_engine.change_account()
                if login_flag:
                    try:
                        posts = self.IA_engine.grapi_engine.user_medias(user_id, 50)
                    except Exception as e:
                        EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                       EventName.Reading_Post_Failed,
                                                       "AccountManager::calculate_statistical",
                                                       robot_api=RobotAPI.Instagrapi, target_account=username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                        return False, False, False, False
                else:
                    EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                                   EventName.All_Changing_Account_Failed,
                                                   "AccountManager::calculate_statistical",
                                                   robot_api=RobotAPI.Instagrapi, target_account=username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id())
                    return False, False, False, False
        likes_count = 0
        comments_count = 0
        post_count = 0
        # for post_item in takewhile(lambda p: p.taken_at.date() > UNTIL,
        #                            dropwhile(lambda p: p.taken_at.date() > SINCE, posts)):
        for post_item in posts:
            if datetime.now(timezone.utc) - post_item.taken_at.astimezone(timezone.utc) < timedelta(days=360):
                post_count += 1
                likes_count += post_item.like_count
                comments_count += post_item.comment_count
        if post_count == 0:
            return 0, 0, 0
        else:
            like_average = (likes_count * 1.0) / post_count
            comment_average = (comments_count * 1.0) / post_count
            activity_per_follower = ((like_average + comment_average) / followers_count) * 100
            return like_average, comment_average, activity_per_follower, post_count

    def update_daily_account_logs(self):
        for acc_id in InflRepo.get_all_infls_acc_id():
            acc_user_id = AccRepo.get_user_id(acc_id)
            acc_username = AccRepo.get_username(acc_id)

            acc_profile, acc_user_id, followers_count, media_count = \
                self.read_account_profile(acc_username, acc_user_id)

            acc_privacy = Privacy.Private if acc_profile.is_private else Privacy.Public

            AVG_Like, AVG_Comment, engagement_rate, post_count = \
                self.calculate_statistical_properties(acc_user_id, followers_count, acc_username)

            AccRepo.register_daily_account_log(acc_id, followers_count, AVG_Like, AVG_Comment, AVG_share,
                                               AVG_save, engagement_rate, stories, media_count, monitoring_status,
                                               acc_privacy, price)
