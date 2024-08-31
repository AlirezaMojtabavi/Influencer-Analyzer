from datetime import datetime, timedelta, timezone, time
from time import sleep
from instagrapi import Client, UserMixin
from time import sleep
from instaloader import instaloader
from Robot import Robot
from InfluencerContainer import InfluencerContainer
import configparser
from Repositories.Influencer_repository import InfluencerRepository


def load_config():
    project_configuration = configparser.ConfigParser()
    project_configuration.read('config.ini')
    return project_configuration

project_config = load_config()
influencer_list_path = project_config.get('Paths', 'influencer_list_path')
account_path = project_config.get('Paths', 'accounts_path')


# insta_loader = instaloader.Instaloader()
# insta_loader.login("mojh.asan", "ssh*1000")
# # influencer_id = insta_loader.check_profile_id(mentioned_username).userid
#
# influencer_profile = insta_loader.check_profile_id("pooorblack")
# followers_count = influencer_profile.followers


engine = Client()
engine.login("Alikamala8", "Alifar1403")
mentioned_username = "jlo"
# sleep(5)
mentioned_id = engine.user_id_from_username(mentioned_username)
mentioned_profile = engine.user_info(mentioned_id)
followers_count_v1 = mentioned_profile.follower_count


IA_robo = Robot(account_path)
influencer_container = InfluencerContainer(IA_robo)

IA_robo.set_influencer_list(influencer_list_path)
# filling influencer_list according to influencer_array
influencer_container.check_infl_array_list(IA_robo.get_influencer_array())

active_infl = influencer_container.get_active_influencers()

infl_repo = InfluencerRepository()
for item in active_infl:
    print(infl_repo.get_username(item) + '\n')

print("bashe")


# engine = Client()
# engine.login("Hoda.noordoost", "Alifartest1403")
# mentioned_username = "jlo"
# # sleep(5)
# mentioned_id = engine.user_id_from_username(mentioned_username)
# mentioned_profile = engine.user_info(mentioned_id)
# followers_count_v1 = mentioned_profile.follower_count
# my_flag = None
# false_flag = False
# # if not my_flag :
# #     print("bashe")
# if not false_flag and false_flag is not None:
#     print("bashe")
# if not my_flag and my_flag is not None:
#     print("bashe")
# sleep(10)  # 10 seconds sleep


#
# sleep(10)
# # influencer_id = insta_loader2.check_profile_id(mentioned_username).userid
#
# influencer_profile2 = insta_loader.check_profile_id(mentioned_username)
# followers_count_new = influencer_profile2.followers

print("bashe")