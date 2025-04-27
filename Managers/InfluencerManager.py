from Repositories.InfluencerRepository import InfluencerRepository as InflRepo, MonitoringStatus
from Repositories.EventRepository import EventRepository, EventCategory, EventType, \
    EventName, RobotAPI
from Repositories.AdvertiseRepository import AdvertiseRepository as AdvRepo
from Repositories.AccountRepository import AccountRepository as AccRepo, Privacy
from datetime import datetime, timezone, timedelta
import random
from time import sleep
from instagrapi.exceptions import PleaseWaitFewMinutes, LoginRequired


class InfluencerManager:
    def __init__(self, bot, acc_manager):
        self.IA_engine = bot
        self.acc_manager = acc_manager

    def create_influencer(self, influencer_username, start_monitoring_datetime, finish_monitoring_datetime, price=None):

        inf_profile, acc_user_id, followers_count, media_count = \
            self.acc_manager.read_account_profile(influencer_username)
        full_name = inf_profile.full_name[:100]
        biography = inf_profile.biography[:200]
        influencer_privacy = Privacy.Private if inf_profile.is_private else Privacy.Public

        like_average, comment_average, activity_per_follower, posts_count = \
            self.acc_manager.calculate_statistical_properties(acc_user_id, followers_count, influencer_username)
        existed_acc_id = AccRepo.check_account_exists(influencer_username)
        if existed_acc_id is not None:
            InflRepo.register_influencer(existed_acc_id, start_monitoring_datetime,
                                         finish_monitoring_datetime, price)
        else:
            new_acc_id = self.acc_manager.create_account(influencer_username, acc_user_id, full_name,
                                                         biography, followers_count, media_count,
                                                         like_average, comment_average, activity_per_follower,
                                                         influencer_privacy)
            InflRepo.register_influencer(new_acc_id, start_monitoring_datetime, finish_monitoring_datetime)

    def read_stories(self, infl_id, reading_stories_flag):
        infl_username = InflRepo.get_username(infl_id)
        infl_user_id = InflRepo.get_user_id(infl_id)
        sleep(random.randint(22, 40))
        try:
            stories = self.IA_engine.grapi_engine.user_stories(infl_user_id)
            EventRepository.register_event(EventType.Log, EventCategory.Reading_Media, EventName.Reading_Story,
                                           "InfluencerManager::read_stories", robot_api=RobotAPI.Instagrapi,
                                           target_account=infl_username, bot_id=self.IA_engine.get_grapi_acc_id())
        except PleaseWaitFewMinutes as e:
            EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                           EventName.Reading_Story_Failed,
                                           "InfluencerManager::read_stories-PleaseWaitFewMinutes",
                                           robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                           bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
            sleep(random.randint(301, 367))  # Wait for 5-6
            # self.IA_engine.grapi_engine.logger.exception(e)
            relogin_flag = self.IA_engine.relogin_grapi("InfluencerManager::read_stories-PleaseWaitFewMinutes",
                                                        infl_username)
            if relogin_flag:
                sleep(random.randint(0, 3))
                try:
                    stories = self.IA_engine.grapi_engine.user_stories(infl_user_id)
                    EventRepository.register_event(EventType.Log, EventCategory.Reading_Media, EventName.Reading_Story,
                                                   "InfluencerManager::read_stories", robot_api=RobotAPI.Instagrapi,
                                                   target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id())
                except Exception as e:
                    EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                   EventName.Reading_Story_Failed,
                                                   "InfluencerManager::read_stories-PleaseWaitFewMinutes",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                    return None, False
            else:
                login_flag = self.IA_engine.change_account()
                if login_flag:
                    sleep(random.randint(0, 3))
                    try:
                        stories = self.IA_engine.grapi_engine.user_stories(infl_user_id)
                        EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                       EventName.Reading_Story, "InfluencerManager::read_stories"
                                                                                "-PleaseWaitFewMinutes",
                                                       robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id())
                    except Exception as e:
                        EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                       EventName.Reading_Story_Failed,
                                                       "InfluencerManager::read_stories-PleaseWaitFewMinutes",
                                                       robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                        return None, False
                else:
                    EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                                   EventName.All_Changing_Account_Failed,
                                                   "InfluencerManager::read_stories-PleaseWaitFewMinutes",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id())
                    return False, False

        except LoginRequired as e:
            EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                           EventName.Reading_Story_Failed,
                                           "InfluencerManager::read_stories-LoginRequired",
                                           robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                           bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))

            # self.IA_engine.grapi_engine.logger.exception(e)
            sleep(random.randint(24, 60))
            relogin_flag = self.IA_engine.relogin_grapi("InfluencerManager::read_stories-LoginRequired",
                                                        infl_username)
            if relogin_flag:
                sleep(random.randint(0, 3))
                try:
                    stories = self.IA_engine.grapi_engine.user_stories(infl_user_id)
                    EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                   EventName.Reading_Story, "InfluencerManager::read_stories-"
                                                                            "LoginRequired",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id())
                except Exception as e:
                    EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                   EventName.Reading_Story_Failed,
                                                   "InfluencerManager::read_stories-LoginRequired",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                    return None, False
            else:
                login_flag = self.IA_engine.change_account()
                if login_flag:
                    sleep(random.randint(0, 3))
                    try:
                        stories = self.IA_engine.grapi_engine.user_stories(infl_user_id)
                        EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                       EventName.Reading_Story, "InfluencerManager::read_stories-"
                                                                                "LoginRequired",
                                                       robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id())
                    except Exception as e:
                        EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                       EventName.Reading_Story_Failed,
                                                       "InfluencerManager::read_stories-LoginRequired",
                                                       robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                        return None, False
                else:
                    EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                                   EventName.All_Changing_Account_Failed,
                                                   "InfluencerManager::read_stories-LoginRequired",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id())
                    return False, False
        except Exception as e:
            EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                           EventName.Reading_Story_Failed,
                                           "InfluencerManager::read_stories-Others",
                                           robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                           bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))

            # self.IA_engine.grapi_engine.logger.exception(e)
            sleep(random.randint(11, 24))
            relogin_flag = self.IA_engine.relogin_grapi("InfluencerManager::read_stories-Others",
                                                        infl_username)
            if relogin_flag:
                sleep(random.randint(1, 3))
                try:
                    stories = self.IA_engine.grapi_engine.user_stories(infl_user_id)
                    EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                   EventName.Reading_Story, "InfluencerManager::read_stories-"
                                                                            "Others",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id())
                except Exception as e:
                    EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                   EventName.Reading_Story_Failed,
                                                   "InfluencerManager::read_stories-Others",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                    return None, False
            else:
                login_flag = self.IA_engine.change_account()
                if login_flag:
                    sleep(random.randint(1, 3))
                    try:
                        stories = self.IA_engine.grapi_engine.user_stories(infl_user_id)
                        EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                       EventName.Reading_Story, "InfluencerManager::read_stories-"
                                                                                "Others",
                                                       robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id())
                    except Exception as e:
                        EventRepository.register_event(EventType.Warning, EventCategory.Reading_Media,
                                                       EventName.Reading_Story_Failed,
                                                       "InfluencerManager::read_stories-Others",
                                                       robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                       bot_id=self.IA_engine.get_grapi_acc_id(), content=str(e))
                        return None, False
                else:
                    EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                                   EventName.All_Changing_Account_Failed,
                                                   "InfluencerManager::read_stories-Others",
                                                   robot_api=RobotAPI.Instagrapi, target_account=infl_username,
                                                   bot_id=self.IA_engine.get_grapi_acc_id())
                    return False, False

        if len(stories) > 0:
            reading_stories_flag = True
        sleep(random.randint(0, 3))
        for story in stories:
            if (datetime.now().astimezone(timezone.utc) - story.taken_at.astimezone(timezone.utc)) < \
                    timedelta(minutes=60) and story.taken_at.astimezone(timezone.utc) > \
                    InflRepo.get_start_monitoring(infl_id).astimezone(timezone.utc):
                if not InflRepo.is_exist_story_id(infl_id, story.id):
                    sleep(random.randint(3, 10))
                    # try:
                    #     self.robo_engine.story_seen([story.pk])
                    # except PleaseWaitFewMinutes as e:
                    #     warning_title = "Story_seen method error on " + infl_username + " stories"
                    #     warning_message = str(e)
                    #     write_warning_message(warning_title, warning_message)
                    #     sleep(random.randint(300, 360))  # Wait for 5-6 minutes
                    #     try:
                    #         self.robo_engine.logger.exception(e)
                    #         sleep(random.randint(30, 60))
                    #         self.robo_engine.relogin()
                    #         write_Log_message(
                    #             "IA robo has relogged in, and skips " + infl_username + "'story_seen method\n" +
                    #             infl_username + "'s stories quantity after relogging: " +
                    #             str(influencer.get_corresponding_stories_count()))
                    #         return
                    #         # self.robo_engine.update_client_settings(self.robo_engine.get_settings())
                    #     except Exception as e:
                    #         error_title = "ReLogin failed"
                    #         error_message = e
                    #         tb = e.__traceback__
                    #         error_line = tb.tb_lineno
                    #         write_error_message(error_title, error_message, error_line)
                    InflRepo.register_story(infl_id, story.id, story.taken_at.astimezone(timezone.utc))
                    mentioned_links = story.mentions
                    for link in mentioned_links:
                        mentioned_user = link.user
                        start_datetime = story.taken_at.astimezone(timezone.utc)
                        mentioned_username = mentioned_user.username
                        adv_acc_id_check = AccRepo.check_account_exists(mentioned_username)
                        adv_id_to_check = AdvRepo.check_advertise_exists(infl_id, adv_acc_id_check)
                        if adv_id_to_check is None:  # story was new:
                            sleep(random.randint(2, 5))
                            self.acc_manager.create_advertise(mentioned_username, infl_id, start_datetime,
                                                              infl_username)
                        else:
                            AdvRepo.plus_story_count(adv_id_to_check)

                sleep(random.randint(2, 6))
        return True, reading_stories_flag

    def get_active_influencers_id(self):
        return InflRepo.get_active_influencers()

    def update_inactive_influencers(self):
        InflRepo.update_inactive_influencers()

    def update_statistical_properties(self):
        incomplete_infl_id = InflRepo.get_incomplete_infl()
        for infl_id in incomplete_infl_id:
            current_user_id = InflRepo.get_user_id(infl_id)
            followers_count = InflRepo.get_follower(infl_id)
            infl_username = InflRepo.get_username(infl_id)
            like_average, comment_average, engagement_rate, posts_count = \
                self.acc_manager.calculate_statistical_properties(current_user_id, followers_count, infl_username)
            if like_average:
                InflRepo.update_statistical_properties(infl_id, like_average, comment_average, engagement_rate)

    def get_all_influencers_id(self):
        return InflRepo.get_all_infl_ids()

    def update_story_table(self):
        InflRepo.update_story_table()

    def check_infl_array_list(self, inf_array_list):
        for influencer_item in inf_array_list:
            influencer_username = influencer_item[1]
            start_monitoring_datetime = influencer_item[2]
            finish_monitoring_datetime = influencer_item[3]
            if len(influencer_item) > 4:
                price = influencer_item[4]
            else:
                price = None

            influencer_id = InflRepo.check_influencer_exists(influencer_username)
            if influencer_id is None:
                self.create_influencer(influencer_username, start_monitoring_datetime,
                                       finish_monitoring_datetime, price)
            else:
                InflRepo.set_monitoring_datetime(influencer_id, start_monitoring_datetime,
                                                 finish_monitoring_datetime)
                if price is not None:
                    InflRepo.update_price(influencer_id, price)


