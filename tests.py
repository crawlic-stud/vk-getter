import shutil
import os

TEST_FOLDER = "tfolder"


def test_imports():
    import vk_getter
    from vk_getter import VKGetter
    import vk_getter.utils
    from vk_getter.utils import download, download_all, download_from_url


def test_download():
    from vk_getter import VKGetter
    from devtest import TOKEN

    getter = VKGetter(TOKEN)
    posts = getter.get_posts("murmewmur", 50)

    from vk_getter.utils import download, download_all, extract, extract_all

    download_all(posts, TEST_FOLDER)
    print(os.listdir(TEST_FOLDER))
    shutil.rmtree(TEST_FOLDER)

    download(posts, "photo", TEST_FOLDER)
    print(os.listdir(f"{TEST_FOLDER}/photos/"))    
    
    photos = extract(posts, "photo")
    all_attachments = extract_all(posts)

    print(photos)
    print(all_attachments)
