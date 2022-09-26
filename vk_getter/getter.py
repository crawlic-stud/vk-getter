from datetime import datetime
import json
import os

from models import Post, Attachments
import utils


class VKGetter:
    """
    Main getter class. Requires a VK access token.
    """

    def __init__(self, token, api_version=5.131):
        self.token = token
        self.api_version = api_version

    def _get_video(self, attachment):
        owner_id = attachment["video"]["owner_id"]
        video_id = attachment["video"]["id"]
        video_url = f"https://api.vk.com/method/video.get?videos={owner_id}_{video_id}" \
                    f"&access_token={self.token}&v={self.api_version}"

        req = utils.get_api(video_url)
        src = req.json()
        files = src["response"]["items"][0]["files"]
        max_quality = list(filter(lambda x: "mp4" in x, files))[-1]
        video_download = files[max_quality]
        return video_download

    def _get_group_id(self, group_domain):
        url = f"https://api.vk.com/method/groups.getById?group_id={group_domain}" \
              f"&access_token={self.token}&v={self.api_version}"
        req = utils.get_api(url)

        group_id = req.json()["response"][0]["id"]
        return group_id

    def get_latest_posts(self, group_domain, count=50,
                         include_pinned=False, include_ads=False, include_copyright=False, allow_no_attachments=False,
                         as_dict=False):
        """Returns a list of Post objects with their id, text, date, time and attachments.

        :param str group_domain: URL or id of a VK group from where posts are taken.
        :param int count: how many posts to take.
        :param bool include_pinned: include pinned post or not.
        :param bool include_ads: include posts with ads or not.
        :param bool include_copyright: include posts with copyright or not.
        :param bool allow_no_attachments: include posts with no attachments or not.
        :param bool as_dict: return posts as dict or as a dataclass object.
        """

        # you can also put a url
        group_domain = group_domain.replace("https://", "").replace("vk.com/", "")

        url = f"https://api.vk.com/method/wall.get?owner_id=-{self._get_group_id(group_domain)}" \
              f"&count={count}&access_token={self.token}&v={self.api_version}"
        req = utils.get_api(url)
        src = req.json()

        fresh_posts = []
        posts = src["response"]["items"]

        for post in posts:
            conditions = [
                not post.get("is_pinned") if not include_pinned else True,
                not post.get("mark_as_ads") if not include_ads else True,
                not post.get("copyright") if not include_copyright else True,
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
                    comments=post["comments"]["count"],
                    likes=post["likes"]["count"],
                    reposts=post["reposts"]["count"],
                    views=post["views"]["count"],
                    )
                )

        if as_dict:
            fresh_posts = utils.get_posts_as_dict(fresh_posts)
        return fresh_posts

    def download_attachments(self, posts, path):
        print("Started collecting photos.")
        for i, post in enumerate(posts):
            photos = post.attachments.photo
            videos = post.attachments.video
            audios = post.attachments.audio
            others = post.attachments.other

            [utils.download_from_url(photo, f"./{path}/photos", f"photo-{i}-{j}") for j, photo in enumerate(photos)]
            [utils.download_from_url(video, f"./{path}/videos", f"video-{i}-{j}") for j, video in enumerate(videos)]
            [utils.download_from_url(audio, f"./{path}/audios", f"audio-{i}-{j}") for j, audio in enumerate(audios)]
            [utils.download_from_url(other, f"./{path}/others", f"other-{i}-{j}") for j, other in enumerate(others)]
