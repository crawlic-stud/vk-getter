import requests

import json
from dataclasses import asdict

from errors import *


def get_req(url):
    req = requests.get(url)
    if req.status_code != 200:
        raise AccessError(f"Bad response: {req.status_code}")
    if req.json().get("error"):
        # hint to where error might be.
        error_url = url.replace('&', '&\n\t\t').replace('?', '?\n\t\t')
        raise RequestError(f"Something went wrong. Error message: {req.json()['error']['error_msg']}"
                           f"\n\nPlease check parameters in the URL below.\n"
                           f"URL: \t{error_url}")
    return req


def get_posts_as_dict(posts_data):
    return [asdict(post) for post in posts_data]


def print_posts_data(posts_data):
    posts = get_posts_as_dict(posts_data)
    json_posts = json.dumps(posts, indent=4, ensure_ascii=False)
    print(json_posts)
    return json_posts
