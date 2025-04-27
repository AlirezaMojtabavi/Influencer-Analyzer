import configparser
from Robot import Robot
from datetime import datetime, timedelta, timezone, time
from time import sleep
import random
from Repositories.EventRepository import EventRepository, EventCategory, EventType, EventName, RobotAPI
from Managers.AdvertiseManager import AdvertiseManager, AdvertiseStatus
from Managers.AccountManager import AccountManager
from Managers.InfluencerManager import InfluencerManager
from Managers.OutputManager import OutputManager
import pytz


def load_config():
    project_configuration = configparser.ConfigParser()
    project_configuration.read('config.ini')
    return project_configuration


project_config = load_config()
influencer_list_path = project_config.get('Paths', 'influencer_list_path')
insta_account_path = project_config.get('Paths', 'accounts_path')
delta_time_1h = timedelta(hours=1)
delta_time_2h = timedelta(hours=2)
delta_time_3h = timedelta(hours=3)
delta_time_12h = timedelta(hours=12)
delta_time_24h = timedelta(hours=24)
xlsx_flag = False

if __name__ == '__main__':
    start_cycle_time_result = datetime.now(timezone.utc)
    login_flag = True
    read_story_flag = True
    followers_count_flag = True
    IA_robo = Robot(insta_account_path)
    acc_manager = AccountManager(IA_robo)
    infl_manager = InfluencerManager(IA_robo, acc_manager)
    output_manager = OutputManager()
    IA_robo.update_influencer_list(influencer_list_path)
    infl_manager.check_infl_array_list(IA_robo.get_influencer_array())
    adv_manager = AdvertiseManager(acc_manager)
    start_story_table_time = datetime.now(timezone.utc)
    infl_manager.update_story_table()

    while True:
        if not IA_robo.get_login_flag():
            break
        current_dif_time_result = datetime.now(timezone.utc) - start_cycle_time_result

        # if datetime.now(timezone.utc).astimezone(pytz.timezone('Asia/Tehran')).time():
        #     acc_manager.update_daily_account_logs()

        if current_dif_time_result > delta_time_3h:
            output_manager.create_xlsx_report()
            IA_robo.update_influencer_list(influencer_list_path)
            infl_manager.check_infl_array_list(IA_robo.get_influencer_array())
            IA_robo.update_bots_account_list(insta_account_path)
            start_cycle_time_result = datetime.now(timezone.utc)
            EventRepository.register_event(EventType.Log, EventCategory.Output_Generation, EventName.Update_Excel_Files,
                                           "Main")
            infl_manager.update_statistical_properties()

        current_dif_time_story_table = datetime.now(timezone.utc) - start_story_table_time
        if current_dif_time_story_table > delta_time_24h:
            infl_manager.update_story_table()
            start_story_table_time = datetime.now(timezone.utc)
            EventRepository.register_event(EventType.Log, EventCategory.Cycle_Management, EventName.Update_Story_Table,
                                           "Main")

        current_dif_time_engine = datetime.now(timezone.utc) - IA_robo.get_start_cycle_time_engine()
        if current_dif_time_engine > delta_time_3h:
            login_flag = IA_robo.change_account()
            if login_flag:
                EventRepository.register_event(EventType.Log, EventCategory.Cycle_Management,
                                               EventName.Cycle_Finished, "Main",
                                               robot_api=RobotAPI.Instagrapi, bot_id=IA_robo.get_grapi_acc_id(),
                                               content="Grapi account changed after engine cycle time")
            else:
                EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                               EventName.All_Changing_Account_Failed, "Main",
                                               robot_api=RobotAPI.Instagrapi, bot_id=IA_robo.get_grapi_acc_id())
                break
        else:
            all_infl_ids = infl_manager.get_all_influencers_id()
            active_infl_ids = infl_manager.get_active_influencers_id()
            infl_manager.update_inactive_influencers()
            reading_stories_flag = False
            # reading_stories_flag = True
            for infl_id in all_infl_ids:
                if infl_id in active_infl_ids:
                    read_story_flag, reading_stories_flag = infl_manager.read_stories(infl_id,
                                                                                      reading_stories_flag)
                    if read_story_flag is None:
                        continue
                    elif not read_story_flag and read_story_flag is not None:
                        break

                for adv_id in adv_manager.get_active_influencer_advertises(infl_id):
                    current_delta_time, mentioned_username = adv_manager.get_delta_time(adv_id)
                    if current_delta_time > delta_time_1h and adv_manager.get_follower_after_1h(adv_id) == 0:
                        followers_count = IA_robo.get_follower_count(mentioned_username, adv_id)
                        if followers_count is None:
                            followers_count = 0
                            continue
                        elif not followers_count and followers_count is not None:
                            followers_count_flag = False
                            break
                        adv_manager.set_follower_after_1h(adv_id, followers_count)
                        EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                       EventName.Reading_Follower_Count, "Main",
                                                       robot_api=RobotAPI.Instaloader,
                                                       target_account=mentioned_username,
                                                       bot_id=IA_robo.get_loader_acc_id(),
                                                       content="Robot read After 1h follower count: " +
                                                               str(followers_count))
                    elif current_delta_time > delta_time_2h and adv_manager.get_follower_after_2h(adv_id) == 0:
                        followers_count = IA_robo.get_follower_count(mentioned_username, adv_id)
                        if followers_count is None:
                            followers_count = 0
                            continue
                        elif not followers_count and followers_count is not None:
                            followers_count_flag = False
                            break
                        adv_manager.set_follower_after_2h(adv_id, followers_count)
                        EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                       EventName.Reading_Follower_Count, "Main",
                                                       robot_api=RobotAPI.Instaloader,
                                                       target_account=mentioned_username,
                                                       bot_id=IA_robo.get_loader_acc_id(),
                                                       content="Robot read After 2h follower count: " +
                                                               str(followers_count))
                    elif current_delta_time > delta_time_12h and adv_manager.get_follower_after_12h(
                            adv_id) == 0:
                        followers_count = IA_robo.get_follower_count(mentioned_username, adv_id)
                        if followers_count is None:
                            followers_count = 0
                            continue
                        elif not followers_count and followers_count is not None:
                            followers_count_flag = False
                            break
                        adv_manager.set_follower_after_12h(adv_id, followers_count)
                        EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                       EventName.Reading_Follower_Count, "Main",
                                                       robot_api=RobotAPI.Instaloader,
                                                       target_account=mentioned_username,
                                                       bot_id=IA_robo.get_loader_acc_id(),
                                                       content="Robot read After 12h follower count: " +
                                                               str(followers_count))
                    elif current_delta_time > delta_time_24h and adv_manager.get_follower_after_24h(
                            adv_id) == 0:
                        followers_count = IA_robo.get_follower_count(mentioned_username, adv_id)
                        if followers_count is None:
                            followers_count = 0
                            continue
                        elif not followers_count and followers_count is not None:
                            followers_count_flag = False
                            break
                        adv_manager.set_follower_after_24h(adv_id, followers_count)
                        EventRepository.register_event(EventType.Log, EventCategory.Reading_Media,
                                                       EventName.Reading_Follower_Count, "Main",
                                                       robot_api=RobotAPI.Instaloader,
                                                       target_account=mentioned_username,
                                                       bot_id=IA_robo.get_loader_acc_id(),
                                                       content="Robot read After 24h follower count: " +
                                                               str(followers_count))
                        adv_manager.set_advertise_status(adv_id, AdvertiseStatus.Close)

            if not reading_stories_flag:
                EventRepository.register_event(EventType.Error, EventCategory.Reading_Media,
                                               EventName.Reading_All_Story_Failed, "Main",
                                               robot_api=RobotAPI.Instagrapi, bot_id=IA_robo.get_grapi_acc_id())
                login_flag = IA_robo.change_account()
                if login_flag:
                    EventRepository.register_event(EventType.Log, EventCategory.Authentication,
                                                   EventName.Login_Succeeded, "Main",
                                                   robot_api=RobotAPI.Instagrapi, bot_id=IA_robo.get_grapi_acc_id(),
                                                   content="Robot logged due to reading_stories_flag")

                else:
                    EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                                   EventName.All_Changing_Account_Failed, "Main",
                                                   robot_api=RobotAPI.Instagrapi, bot_id=IA_robo.get_grapi_acc_id(),
                                                   content="Robot all changing account failed due to "
                                                           "reading_stories_flag")
                    break
            if not read_story_flag and read_story_flag is not None:
                break
            if not followers_count_flag and followers_count_flag is not None:
                break

        EventRepository.register_event(EventType.Log, EventCategory.Cycle_Management,
                                       EventName.Cycle_Finished, "Main")
        sleep(random.randint(40, 60))

    # write_error_message("The pipeline has been broken")
    output_manager.create_xlsx_report()
    EventRepository.register_event(EventType.Error, EventCategory.Cycle_Management,
                                   EventName.Robot_Stopped, "Main", bot_id=IA_robo.get_grapi_acc_id())
