import shutil
import os

import requests

from ..models import Post


def _assert_query(query):
    if query not in ["photo", "video", "audio", "other"]:
        raise TypeError("Query must be one of the following: photo, video, audio, other.")


def download_from_url(url: str, folder: str, filename: str) -> bytearray:
    """Downloads file from url to a specified folder, returns file's binary data."""
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
    return req.raw


def download_all(posts: list[Post], path: str) -> None:
    """Downloads all attachments for list of posts into path specified."""
    for i, post in enumerate(posts):
        [download_from_url(photo, f"./{path}/photos", f"photo{i}{j}") for j, photo in enumerate(post.attachments.photo)]
        [download_from_url(video, f"./{path}/videos", f"video{i}{j}") for j, video in enumerate(post.attachments.video)]
        [download_from_url(audio, f"./{path}/audios", f"audio{i}{j}") for j, audio in enumerate(post.attachments.audio)]
        [download_from_url(other, f"./{path}/others", f"other{i}{j}") for j, other in enumerate(post.attachments.other)]


def download(posts: list[Post], query: str, path: str) -> None:
    """Downloads attachments of specified type (photo, video, audio, other)."""
    _assert_query(query)
    for i, post in enumerate(posts):
        [download_from_url(attach, f"./{path}/{query}s", f"{query}{i}{j}") 
            for j, attach in enumerate(getattr(post.attachments, query))]
    

def extract_all(posts):
    """Extracts all attachments of given posts."""
    photos = []
    videos = []
    audios = []
    others = []
    for post in posts:
        photos += post.attachments.photo
        videos += post.attachments.video
        audios += post.attachments.audio
        others += post.attachments.other
    return photos, videos, audios, others


def extract(posts, query):
    """Extracts attachments of specified type (photo, video, audio, other)."""
    _assert_query(query)
    attachments = []
    for post in posts:
        attachments += getattr(post.attachments, query)
    return attachments
