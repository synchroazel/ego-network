import json
from time import sleep

import requests
from tqdm import tqdm

<<<<<<< HEAD
bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAALtoawEAAAAAsWsPhiKWaFzeFs7yw73TCEK9ZnY' \
               '%3D3JHfPs7T3H645LpQri2bxWc6iMpVivbxe0zINLLcEnfkI4OKsi'

payload = {}
headers = {
    'Authorization': bearer_token,
    'Cookie': 'guest_id=v1%3A164848202636275073'
=======
from secrets import bearer_token

payload = {}
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Cookie': ''
>>>>>>> 58011a5 (new, reviewed version)
}


class TwitterUser:

    def __init__(self, username):
        url = f"https://api.twitter.com/1.1/users/show.json?screen_name={username}"
        response = requests.request("GET", url, headers=headers, data=payload)
        cur_json = json.loads(response.text)
        self.id = cur_json["id"]
        self.user = username
        self.name = cur_json["name"]
        self.followers_count = cur_json["followers_count"]
        self.following_count = cur_json["friends_count"]
        self.followers = []  # storing list of followers
        self.following = []  # storing list of following
        self.json = cur_json

    def get(self, obj, max_results=1000, all=False, dtime=1):
        """
        Fetch followers/following in a list of dicts.

        :param obj: accept 'followers' and 'following'
        :param max_results: max number of results (1000 is the max set by the API)
                            (if using all=True, max_results is the max number of results for each request)
        :param all: True if you want to get all followers/following
        :param dtime: idle time between requests (in minutes)
        """

        assert obj == 'followers' or obj == 'following', \
            'Please specify followers or following.'

        if obj == 'followers':
            iterations = range((self.followers_count // max_results) + 1)
        if obj == 'following':
            iterations = range((self.following_count // max_results) + 1)

        next_token = ""

        for _ in tqdm(iterations, disable=not all, desc=f'Getting {obj}'):
            url = f"https://api.twitter.com/2/users/{str(self.id)}/{obj}?max_results={str(max_results)}{next_token}"
            response = requests.request("GET", url, headers=headers, data=payload)
            cur_json = json.loads(response.text)

            if "meta" not in cur_json.keys():
                print(cur_json["detail"])
                break

            if obj == 'followers':
                self.followers.extend(cur_json["data"])
            if obj == 'following':
                self.following.extend(cur_json["data"])

            if "next_token" in cur_json["meta"]:
                next_token = "&pagination_token=" + cur_json["meta"]["next_token"]

            if not all:
                break

            sleep(60 * dtime)

    def dump(self, obj):
        """
        Dump fetched list of followers/following in a .json file.

        :param obj: what to dump in a .json - accept 'followers','following' and 'all
        """

        assert obj == 'followers' or obj == 'following' or obj == 'all', \
            'Please specify what to dump.\nfollowers / following / all'

        if obj == 'followers':
            with open('egonet_followers.json', 'w') as f:
                json.dump(dict(self.followers), f, indent=4)

        if obj == 'following':
            with open('egonet_following.json', 'w') as f:
                json.dump(dict(self.following), f, indent=4)

        if obj == 'all':
            db_dict = {
                'ego': self.json,
                'followers': self.followers,
                'following': self.following
            }

            with open('egonet_db.json', 'w') as f:
                json.dump(db_dict, f, indent=4)
