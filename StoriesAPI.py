import requests


def get_instagram_stories(ig_user_id, access_token):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/stories"
    # url = "https://www.instagram.com/stories/sabamorshedii"
    url = "https://graph.facebook.com/v20.0/me?fields=name&access_token={EAAFsoyZAlAuABOzzYJA49itT01iNKHOWrDIXLUkIk9pKumd4Gb3N9eKQZBJNm1QDe0vWtQJcHo7ZC6MtquUDVqZBFGn0PaZBYUiF2TfD92gbvki4uU95tQGqs7Ev5VfS3oSEO9BDmoRnZC3hSBkczahD7qenqeKjoJ6usKz1zqdZAGvOe9n5GJMc2ytrbuPuHP8Fui4Am113qHAfbR0Jdj9ZCGMNyOoZD}"
    params = {
        'access_token': access_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        stories = data.get('data', [])
        story_ids = [story['id'] for story in stories]
        return story_ids
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None


def get_bio(instagram_user_id, access_token):
    # Instagram Graph API endpoint to get user info
    url = f'https://graph.instagram.com/{instagram_user_id}?fields=biography&access_token={access_token}'


    # Making a GET request to the Instagram Graph API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        user_info = response.json()
        print("User Biography:", user_info['biography'])
    else:
        print("Failed to retrieve information:", response.status_code, response.text)


ig_user_id = '5434962520'

access_token = 'EAAFsoyZAlAuABOzzYJA49itT01iNKHOWrDIXLUkIk9pKumd4Gb3N9eKQZBJNm1QDe0vWtQJcHo7ZC6MtquUDVqZBFGn0PaZBYUiF2TfD92gbvki4uU95tQGqs7Ev5VfS3oSEO9BDmoRnZC3hSBkczahD7qenqeKjoJ6usKz1zqdZAGvOe9n5GJMc2ytrbuPuHP8Fui4Am113qHAfbR0Jdj9ZCGMNyOoZD'
# stories = get_instagram_stories(ig_user_id, access_token)
get_instagram_stories(5434962520, access_token)
# if stories:
#     print(stories)
