import requests

import os
import json
from dataclasses import asdict
import shutil

from .errors import *


def get_api(url):
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


def download_from_url(url, folder, filename):
    try:
        req = requests.get(url, stream=True)
    except requests.exceptions.MissingSchema:
        return

    if req.status_code == 200:
        _, extension = req.headers.get('content-type').split("/")
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"{filename}.{extension}"
        with open(os.path.join(folder, filename), 'wb') as f:
            shutil.copyfileobj(req.raw, f)
