from instagrapi import Client
from instagrapi.exceptions import PleaseWaitFewMinutes, LoginRequired
import openpyxl
from time import sleep
from instaloader import instaloader
import random
from datetime import datetime, timezone
from Repositories.EventRepository import EventRepository
from Repositories.BotRepository import BotRepository
from Models.Event import EventName, EventCategory, RobotAPI, EventType
from instagrapi.types import (
    Account, Collection, Comment, DirectMessage, DirectThread, Hashtag, Highlight, Location, Media, MediaOembed,
    Share, Story, StoryLink, StoryMedia, StoryMention, StorySticker, User, UserShort, Usertag,
)

from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    RecaptchaChallengeForm,
    ReloginAttemptExceeded,
    SelectContactPointRecoveryForm,
)


class Robot:
    def __init__(self, accounts_path):
        self.grapi_username = ""
        self.grapi_password = ""
        self.influencer_array = []
        self.account_array = []
        self.grapi_account_id = None
        self.start_cycle_time_engine = None
        self.set_authentication(accounts_path)
        self.grapi_engine = None
        self.engine_flag = None
        self.loader_account_id = None
        self.engine_flag = self.set_grapi_engine()
        self.loader_username = ""
        self.loader_password = ""
        self.loader_engine = None
        if self.engine_flag:
            self.prepare_loader_engine()
            self.start_cycle_time_engine = datetime.now(timezone.utc)

    def set_authentication(self, accounts_path):
        self.set_accounts_list(accounts_path)
        self.grapi_username = self.account_array[0][1]
        self.grapi_password = self.account_array[0][2]
        self.grapi_account_id = 1

    def set_grapi_engine(self):
        self.grapi_engine = Client()
        # self.engine.user_info()
        try:
            self.grapi_engine.login(self.grapi_username, self.grapi_password)
            # write_Log_message("IA engine has logged in successfully\nAccount:\t" + self.username)
            EventRepository.register_event(EventType.Log, EventCategory.Authentication,
                                           EventName.Login_Succeeded, "Robot::set_grapi_engine",
                                           robot_api=RobotAPI.Instagrapi, bot_id=self.get_grapi_acc_id(),
                                           content="Robot logged")
            return True
        except Exception as e:
            # error_title = "Failed to logging in " + self.username + " account"
            # write_warning_message(error_title, str(e))
            EventRepository.register_event(EventType.Warning, EventCategory.Authentication,
                                           EventName.Login_Failed, "Robot::set_grapi_engine",
                                           robot_api=RobotAPI.Instagrapi, bot_id=self.get_grapi_acc_id(),
                                           content=str(e))
            login_flag = self.change_account()
            if login_flag:
                return True
            else:
                # write_error_message("Changing grapi accounts failed", "Last account: " + self.username)
                EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                               EventName.All_Changing_Account_Failed, "Robot::set_grapi_engine",
                                               robot_api=RobotAPI.Instagrapi, bot_id=self.get_grapi_acc_id())
                return False

    def prepare_loader_engine(self):
        if self.grapi_account_id >= len(self.account_array):
            self.loader_account_id = 1
        else:
            self.loader_account_id = self.grapi_account_id + 1
        self.loader_username = self.account_array[self.loader_account_id - 1][1]
        self.loader_password = self.account_array[self.loader_account_id - 1][2]
        self.loader_engine = instaloader.Instaloader()
        try:
            self.loader_engine.login(self.loader_username, self.loader_password)
            # write_Log_message(
            #     "IA follower_counter_engine has logged in successfully\nAccount:\t" + self.second_username)
            EventRepository.register_event(EventType.Log, EventCategory.Authentication,
                                           EventName.Login_Succeeded, "Robot::prepare_loader_engine",
                                           robot_api=RobotAPI.Instaloader, bot_id=self.get_loader_acc_id(),
                                           content="Robot logged")
            return True
        except Exception as e:
            # warnig_title = "Failed to logging in " + self.second_username + " account for follower_counter_engine"
            # write_warning_message(warnig_title, str(e))
            EventRepository.register_event(EventType.Warning, EventCategory.Authentication,
                                           EventName.Login_Failed, "Robot::prepare_loader_engine",
                                           robot_api=RobotAPI.Instaloader, bot_id=self.get_loader_acc_id(),
                                           content=str(e))
            login_flag = self.change_account()
            if login_flag:
                return True
            else:
                # write_error_message("Changing loader accounts failed", "Last account: " + self.second_username)
                EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                               EventName.All_Changing_Account_Failed, "Robot::prepare_loader_engine",
                                               robot_api=RobotAPI.Instaloader, bot_id=self.get_loader_acc_id())
                return False

    def get_engine(self):
        return self.grapi_engine

    def set_influencer_list(self, influencer_list_path):
        workbook = openpyxl.load_workbook(influencer_list_path)
        sheet = workbook.active
        for row in range(2, 9000):
            if sheet.cell(row, 1).value:
                row_id = int(sheet.cell(row, 1).value)
                user = sheet.cell(row, 2).value
                start_date = sheet.cell(row, 3).value
                end_date = sheet.cell(row, 4).value
                price = sheet.cell(row, 5).value
                if price is not None:
                    self.influencer_array.append([row_id, user, start_date.astimezone(timezone.utc),
                                              end_date.astimezone(timezone.utc), price])
                else:
                    self.influencer_array.append([row_id, user, start_date.astimezone(timezone.utc),
                                              end_date.astimezone(timezone.utc)])
            else:
                break

    def set_accounts_list(self, accounts_path):
        self.account_array.clear()
        # try:
        workbook = openpyxl.load_workbook(accounts_path)
        # except Exception as e:
        #     error_title = "Failed to reading accounts Excel file"
        #     error_message = e
        #     write_error_message(error_title, error_message)
        sheet = workbook.active
        for row in range(2, sheet.max_row):
            if sheet.cell(row, 1).value:
                row_id = int(sheet.cell(row, 1).value)
                username = str(sheet.cell(row, 2).value)
                password = str(sheet.cell(row, 3).value)
                phone_num = str(sheet.cell(row, 3).value)
                self.account_array.append([row_id, username, password])
            else:
                break

    def get_influencer_array(self):
        return self.influencer_array

    def change_grapi_account(self):
        if self.grapi_account_id >= len(self.account_array) and self.loader_account_id != 1:
            self.grapi_account_id = 1
        elif self.grapi_account_id >= len(self.account_array) and self.loader_account_id == 1:
            self.grapi_account_id = self.loader_account_id + 1
        elif self.grapi_account_id + 1 == self.loader_account_id and self.loader_account_id >= len(self.account_array):
            self.grapi_account_id = 1
        elif self.grapi_account_id + 1 == self.loader_account_id and self.loader_account_id < len(self.account_array):
            self.grapi_account_id += 2
        else:
            self.grapi_account_id += 1

        self.grapi_username = self.account_array[self.grapi_account_id - 1][1]
        self.grapi_password = self.account_array[self.grapi_account_id - 1][2]
        try:
            self.grapi_engine.logout()
            sleep(random.randint(9, 20))
            self.grapi_engine = Client()
            self.grapi_engine.username = self.grapi_username
            self.grapi_engine.password = self.grapi_password
            self.grapi_engine.login(self.grapi_username, self.grapi_password)
            # write_Log_message("IA engine has logged in successfully by " + self.username + " account")
            EventRepository.register_event(EventType.Log, EventCategory.Authentication,
                                           EventName.Login_Succeeded, "Robot::change_grapi_account",
                                           robot_api=RobotAPI.Instagrapi, bot_id=self.get_grapi_acc_id(),
                                           content="Robot logged")
            self.start_cycle_time_engine = datetime.now(timezone.utc)
            sleep(random.randint(4, 17))
            return True
        except Exception as e:
            # warning_title = "login failed for grapi accounts\n" + self.username + " couldn't login"
            # write_warning_message(warning_title, str(e))
            EventRepository.register_event(EventType.Warning, EventCategory.Authentication,
                                           EventName.Login_Failed, "Robot::change_grapi_account",
                                           robot_api=RobotAPI.Instagrapi, bot_id=self.get_grapi_acc_id(),
                                           content=str(e))
            return False

    def change_account(self, engine_type="grapi"):
        login_trying_number = 0
        login_flag = True
        if engine_type == "grapi":
            while login_trying_number < self.get_reserved_accounts_count():
                login_trying_number += 1
                if self.change_grapi_account():
                    return True
                else:
                    login_flag = False
                    sleep(45)
                if login_trying_number > 4:
                    # write_error_message("Faild to change grapi account",
                    #                         "\nlogin_trying_number: " + str(login_trying_number) +
                    #                     "\n" + self.username)
                    EventRepository.register_event(EventType.Warning, EventCategory.Authentication,
                                                   EventName.Login_Failed, "Robot::change_account",
                                                   robot_api=RobotAPI.Instagrapi, bot_id=self.get_grapi_acc_id(),
                                                   content="Changing account trying number: " + str(login_trying_number))

            if not login_flag:
                return False
        else:
            while login_trying_number < self.get_reserved_accounts_count():
                login_trying_number += 1
                if self.change_loader_account():
                    return True
                else:
                    login_flag = False
                    sleep(35)
                if login_trying_number > 4:
                    # write_error_message("Faild to change loader account", "\nlogin_trying_number: " + str(
                    # login_trying_number) + "\n" + self.second_username)
                    EventRepository.register_event(EventType.Warning, EventCategory.Authentication,
                                                   EventName.Login_Failed, "Robot::change_account",
                                                   robot_api=RobotAPI.Instaloader, bot_id=self.get_loader_acc_id(),
                                                   content="Changing account trying number: " + str(
                                                       login_trying_number))
            if not login_flag:
                return False

    def change_loader_account(self):
        if self.loader_account_id >= len(self.account_array) and self.grapi_account_id != 1:
            self.loader_account_id = 1
        elif self.loader_account_id >= len(self.account_array) and self.grapi_account_id == 1:
            self.loader_account_id = self.grapi_account_id + 1
        elif self.loader_account_id + 1 == self.grapi_account_id and self.grapi_account_id >= len(self.account_array):
            self.loader_account_id = 1
        elif self.loader_account_id + 1 == self.grapi_account_id and self.grapi_account_id < len(self.account_array):
            self.loader_account_id += 2
        else:
            self.loader_account_id += 1

        self.loader_username = self.account_array[self.loader_account_id - 1][1]
        self.loader_password = self.account_array[self.loader_account_id - 1][2]
        try:
            self.loader_engine = instaloader.Instaloader()
            self.loader_engine.login(self.loader_username, self.loader_password)
            # write_Log_message("IA follower_counter_engine has logged in successfully by " +
            #                   self.second_username + " account")
            EventRepository.register_event(EventType.Log, EventCategory.Authentication,
                                           EventName.Login_Succeeded, "Robot::change_loader_account",
                                           robot_api=RobotAPI.Instaloader, bot_id=self.get_loader_acc_id(),
                                           content="Robot logged")
            sleep(random.randint(4, 17))
            return True
        except Exception as e:
            # warning_title = "login failed\n" + self.second_username + " couldn't log in for follower_counter_engine"
            # write_warning_message(warning_title, str(e))
            EventRepository.register_event(EventType.Warning, EventCategory.Authentication,
                                           EventName.Login_Failed, "Robot::change_loader_account",
                                           robot_api=RobotAPI.Instaloader, bot_id=self.get_loader_acc_id(), content=str(e))
            return False

    def get_reserved_accounts_count(self):
        return len(self.account_array)

    def get_login_flag(self):
        return self.engine_flag

    def get_follower_count(self, mentioned_username, adv_id):
        try:
            mentioned_profile = self.loader_engine.check_profile_id(mentioned_username)
            followers_count = mentioned_profile.followers
            return followers_count
        except Exception as e:
            # error_title = "Failed to get followers_count by \n" + self.second_username + " for " + mentioned_username
            # write_warning_message(error_title, str(e))
            EventRepository.register_event(EventType.Error, EventCategory.Reading_Media,
                                           EventName.Reading_Profile_Failed, "Robot::get_follower_count",
                                           robot_api=RobotAPI.Instaloader, target_account=mentioned_username,
                                           bot_id=self.get_loader_acc_id(), content=str(e))
            login_flag = self.change_account("instaloader")
            if login_flag:
                try:
                    mentioned_profile = self.loader_engine.check_profile_id(mentioned_username)
                    followers_count = mentioned_profile.followers
                    return followers_count
                except Exception as e:
                    # write_error_message("IA follower engine couldn't get the value\n" +
                    #                       "Loader account: " + self.second_username + "\nmentioned account: " +
                    #                       mentioned_username, str(e))
                    EventRepository.register_event(EventType.Error, EventCategory.Reading_Media,
                                                   EventName.Reading_Profile_Failed,
                                                   "Robot::get_follower_count",
                                                   robot_api=RobotAPI.Instaloader, target_account=mentioned_username,
                                                   bot_id=self.get_loader_acc_id(), content=str(e))
                    return None

            else:
                # write_error_message("Changing loader accounts failed", "Last account: " + self.second_username)
                EventRepository.register_event(EventType.Error, EventCategory.Authentication,
                                               EventName.All_Changing_Account_Failed, "Robot::get_follower_count",
                                               robot_api=RobotAPI.Instaloader, bot_id=self.get_loader_acc_id())
                return False

    def get_start_cycle_time_engine(self):
        return self.start_cycle_time_engine

    def update_cycle_time_engine(self):
        self.start_cycle_time_engine = datetime.now(timezone.utc)

    def get_grapi_acc_id(self):
        return BotRepository.get_bot_id(self.grapi_username)

    def get_loader_acc_id(self):
        return BotRepository.get_bot_id(self.loader_username)