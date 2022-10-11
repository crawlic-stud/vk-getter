import shutil
import os
from unittest import TextTestResult

TEST_FOLDER = "tfolder"


def test_imports():
    import vk_getter
    from vk_getter import VKGetter
    import vk_getter.utils
    from vk_getter.utils import download_from_url, get_api


def test_download():
    from vk_getter import VKGetter
    from devtest import TOKEN

    getter = VKGetter(TOKEN)
    posts = getter.get_posts("crawlic", 50)

    photos_folder = f"{TEST_FOLDER}/photo"

    # test that it creates all necessary folders and download files to them
    getter.download_all(posts, TEST_FOLDER)
    print(os.listdir(TEST_FOLDER))
    assert len(os.listdir(TEST_FOLDER)) > 0
    created_folders = os.listdir(TEST_FOLDER)
    for folder in created_folders:
        assert len(os.listdir(f"{TEST_FOLDER}/{folder}")) > 0 
    shutil.rmtree(TEST_FOLDER)

    # test photos specifically
    getter.download(posts, "photo", TEST_FOLDER)
    print(os.listdir(photos_folder))
    assert len(os.listdir(photos_folder)) > 0
    shutil.rmtree(TEST_FOLDER)

    # test if it extracts photos and other attachments
    photos = getter.extract(posts, "photo")
    attachments = getter.extract_all(posts)

    print(photos)
    print(attachments)
