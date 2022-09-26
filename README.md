# VK Getter

Very simple and pythonic way to extract data from https://www.vk.com

## Getting started

Install package via pip

```
pip install vk_getter
```

Extract latest posts from any vk group domain

```python
from vk_getter import VKGetter

getter = VKGetter("YOUR TOKEN")
group_domain = "vk" # same as https://www.vk.com/vk

posts = getter.get_latest_posts(group_domain=group_domain
                                count=1,
                                include_pinned=False,
                                allow_no_attachments=False,
                                include_ads=False,
                                include_copyright=False)
```

Retrieved posts are retrieved as Python dataclass, but can also be returned as dictionary.

```python
from vk_getter import VKGetter

getter = VKGetter("YOUR TOKEN")
posts = getter.get_latest_posts(group_domain="vk",
                                count=1,
                                as_dict=True)
# posts[0] = 
#     {
#         "id": 1320761,
#         "date": "15.09.2022",
#         "time": "14:15:11",
#         "text": "...",
#         "attachments": {
#             "photo": [],
#             "video": [
#                 "..."
#             ],
#             "audio": [],
#             "other": []
#         },
#         "comments": 858,
#         "likes": 1150,
#         "reposts": 371,
#         "views": 518953
#     }

```

Also, you can download all the gathered attachments to your local system.

```python
from vk_getter import VKGetter

getter = VKGetter("YOUR TOKEN")
posts = getter.get_latest_posts(group_domain="lol",
                                count=100)

getter.download_attachments(posts, path="some_folder")
```
`*Note:` do NOT use `as_dict` in this method.