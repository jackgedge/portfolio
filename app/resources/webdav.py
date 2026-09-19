from typing import Any
from tempfile import _TemporaryFileWrapper
from flask.cli import load_dotenv
from webdav3.client import Client
from pathlib import Path
import os 
import tempfile
import random
from PIL import Image

from app import PORTFOLIO_DIR, THUMBNAIL_DIR, IMAGE_FORMATS

# Define WebDav options
hostname: str | None = os.getenv('WEBDAV_HOSTNAME')
login: str | None = os.getenv('WEBDAV_LOGIN')
password: str | None = os.getenv('WEBDAV_PASSWORD')

options: dict[str | None, str | None] = {
    'webdav_hostname': hostname,
    'webdav_login': login,
    'webdav_password': password
}

# Create WebDav client
client = Client(options)


def get_folders():
    folders = client.list(PORTFOLIO_DIR)[1:]
    folders_clean = []
    for folder_name in folders:
        folders_clean.append(folder_name.strip('/'))

        #TODO Remove unwanted folders

    return folders_clean


def clean_images(images):

    clean_image_list = [] 

    clean_image_list: list[str] = [
        image
        for image in images
        if image.lower().endswith(tuple(IMAGE_FORMATS))
    ]
    return clean_image_list


def get_folder_images(folder):
    folder_path: str = f"{PORTFOLIO_DIR}/{folder}"
    images = client.list(folder_path)[1:]
    
    clean_image_list = clean_images(images)

    return clean_image_list


def get_folder_thumbnails(folder):
    thumbnail_folder_path: str = f"{PORTFOLIO_DIR}/{folder}/{THUMBNAIL_DIR}"
    thumbnails = client.list(thumbnail_folder_path)[1:]
    clean_thumbnail_list = clean_images(thumbnails)
    return clean_thumbnail_list


def get_image(folder, image):
    remote_path: str = (
        f"{PORTFOLIO_DIR.rstrip('/')}/"
        f"{folder.strip('/')}/"
        f"{image.lstrip('/')}"
    )

    extension = os.path.splitext(image)[1]

    temp_file: _TemporaryFileWrapper[bytes]= tempfile.NamedTemporaryFile(
        suffix=extension,
        delete=False,
    )
    temp_path = temp_file.name
    temp_file.close()

    try:
        client.download_sync(
            remote_path=remote_path,
            local_path=temp_path,
        )
        return temp_path

    except Exception:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass
        raise


def get_thumbnail(folder, thumbnail):
    remote_path: str = (
        f"{PORTFOLIO_DIR.rstrip('/')}/"
        f"{folder.strip('/')}/.thumbnails/"
        f"{thumbnail.lstrip('/')}"
    )

    extension = os.path.splitext(thumbnail)[1]

    temp_file: _TemporaryFileWrapper[bytes]= tempfile.NamedTemporaryFile(
        suffix=extension,
        delete=False,
    )
    temp_path = temp_file.name
    temp_file.close()

    try:
        client.download_sync(
            remote_path=remote_path,
            local_path=temp_path,
        )
        return temp_path

    except Exception:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass
        raise


def get_random_images(thumbnails=False):
    folders = client.list(PORTFOLIO_DIR)[1:]

    all_images: list[str] = []

    for raw_folder in folders:
        folder = raw_folder.strip("/")

        if thumbnails == False:
            folder_path: str = (
                f"{PORTFOLIO_DIR.rstrip('/')}/"
                f"{folder}"
            )
        else:
            folder_path: str = (
                f"{PORTFOLIO_DIR.rstrip('/')}/"
                f"{folder}/"
                f"{THUMBNAIL_DIR}"
            )

        images = client.list(folder_path)[1:]

        for raw_image in images:
            image = raw_image.strip("/")

            if image.lower().endswith(tuple(IMAGE_FORMATS)):
                all_images.append({
                    "folder": folder,
                    "image": image,
                })

    return random.sample(
        all_images,
        min(15, len(all_images))
    )