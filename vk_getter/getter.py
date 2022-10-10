from datetime import datetime
import math

import requests

from .models import Post, Attachments
from . import utils


class VKGetter:
    """
    Main getter class. Requires a VK access token.
    """

    def __init__(self, token, api_version=5.131):
        self.token = token
        self.api_version = api_version
        self.session = requests.Session()

    def _get_video(self, attachment):
        owner_id = attachment["video"]["owner_id"]
        video_id = attachment["video"]["id"]
        video_url = f"https://api.vk.com/method/video.get?videos={owner_id}_{video_id}" \
                    f"&access_token={self.token}&v={self.api_version}"
        req = utils.get_api(video_url, self.session)
        src = req.json()
        files = src["response"]["items"][0]["files"]
        max_quality = list(filter(lambda x: "mp4" in x, files))[-1]
        video_download = files[max_quality]
        return video_download

    def _get_group_id(self, group_domain):
        url = f"https://api.vk.com/method/groups.getById?group_id={group_domain}" \
              f"&access_token={self.token}&v={self.api_version}"
        req = utils.get_api(url, self.session)

        group_id = req.json()["response"][0]["id"]
        return group_id

    def _get_wall_with_offset(self, group_id, count, offset):
        url = f"https://api.vk.com/method/wall.get?owner_id=-{group_id}" \
              f"&count={count}&offset={offset}&access_token={self.token}&v={self.api_version}"
        req = utils.get_api(url, self.session)
        return req.json()

    def get_raw_posts(self, group_domain, count, offset=0):
        """Returns list of posts in raw format, just like in vk api."""
        # you can also put a url
        group_domain = group_domain.replace("https://", "").replace("vk.com/", "")
        group_id = self._get_group_id(group_domain)

        posts = []
        for _ in range(count // 100):
            next_posts = self._get_wall_with_offset(group_id, count, offset)
            posts += next_posts["response"]["items"]
            offset += 100

        left_over = count - offset
        if left_over:
            next_posts = self._get_wall_with_offset(group_id, left_over, offset)
            posts += next_posts["response"]["items"]

        return posts


    def get_posts(self, group_domain, count, offset=0,
                        pinned=False, ads=False, copyright=False, allow_no_attachments=False,
                        as_dict=False):
        """Returns a list of Post objects with their id, text, date, time and attachments.

        :param str group_domain: URL or id of a VK group from where posts are taken.
        :param int count: how many posts to take.
        :param bool pinned: include pinned post or not.
        :param bool ads: include posts with ads or not.
        :param bool copyright: include posts with copyright or not.
        :param bool allow_no_attachments: include posts with no attachments or not.
        :param bool as_dict: return posts as dict or as a dataclass object.
        """

        posts = self.get_raw_posts(group_domain, count, offset)
        fresh_posts = []

        for post in posts:
            # check each post to meet certain conditions
            conditions = [
                not post.get("is_pinned") if not pinned else True,
                not post.get("mark_as_ads") if not ads else True,
                not post.get("copyright") if not copyright else True,
                post.get("attachments") if not allow_no_attachments else True
            ]
            # print(json.dumps(post, indent=4, ensure_ascii=False))
            if all(conditions):
                attachments = post.get("attachments", [])
                photo_attachments = []
                video_attachments = []
                audio_attachments = []
                other_attachments = []

                for attachment in attachments:
                    try:
                        if attachment["type"] == "photo":
                            photo_attachments.append(attachment["photo"]["sizes"][4]["url"])
                        elif attachment["type"] == "video":
                            video_attachments.append(self._get_video(attachment))
                        elif attachment["type"] == "audio":
                            audio_attachments.append(attachment[attachment["type"]]["url"])
                        else:
                            other_attachments.append(attachment[attachment["type"]]["url"])
                    except (IndexError, KeyError):
                        pass

                date = datetime.fromtimestamp(post["date"]).strftime("%d.%m.%Y")
                time = datetime.fromtimestamp(post["date"]).strftime("%H:%M:%S")
                fresh_posts.append(Post(
                    id=post["id"],
                    date=date,
                    time=time,
                    text=post["text"],
                    attachments=Attachments(
                        photo=photo_attachments,
                        video=video_attachments,
                        audio=audio_attachments,
                        other=other_attachments
                        ),
                    comments=post.get("comments", {}).get("count", 0),
                    likes=post.get("likes", {}).get("count", 0),
                    reposts=post.get("reposts", {}).get("count", 0),
                    views=post.get("views", {}).get("count", 0),
                    )
                )

        if as_dict:
            fresh_posts = utils.get_posts_as_dict(fresh_posts)
        return fresh_posts
