from dataclasses import dataclass


@dataclass(frozen=True)
class Video:
    download: str
    player: str


@dataclass(frozen=True)
class Attachment:
    photo: list[str]
    video: list[Video]
    other: list[str]


@dataclass(frozen=True)
class Post:
    id: int
    date: str
    time: str
    text: str
    attachments: Attachment
    comments: int = 0
    likes: int = 0
    reposts: int = 0
    views: int = 0
