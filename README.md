# VK Getter

Very simple and pythonic way to extract data from https://www.vk.com

## Getting started

Install package via pip

```
pip install vk_getter
```

Firstly, you need to get your access token. You can get it [here](https://vkhost.github.io/).

Just paste your token into a getter and you good to go!
```python
from vk_getter import VKGetter

getter = VKGetter("TOKEN")

# get 100 posts from https://www.vk.com/vk
posts = getter.get_latest_posts("vk", 100) 
```

You can specify different settings:

```python
posts = getter.get_latest_posts(group_domain="https://www.vk.com/vk"
                                count=1,
                                include_pinned=False,
                                allow_no_attachments=False,
                                include_ads=False,
                                include_copyright=False)
```

All posts are retrieved as Python dataclasses, but can also be returned as dictionaries.

```python
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
from vk_getter.utils import download_attachments

posts = getter.get_latest_posts("lol", 15)
getter.download_attachments(posts, path="images")
```
`*Note:` do NOT use `as_dict` in this method.

***