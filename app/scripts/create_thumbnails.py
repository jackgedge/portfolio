from tempfile import _TemporaryFileWrapper
from flask.cli import load_dotenv
from webdav3.client import Client
from pathlib import Path
import os 
import tempfile
from PIL import Image

from app.resources.webdav import client
from app import PORTFOLIO_DIR, THUMBNAIL_DIR

# Get list of portfolio contents
portfolio_list = client.list(PORTFOLIO_DIR)[1:]

image_folders = [item for item in portfolio_list if item.endswith("/")]

# Iterate through image folders
for image_folder in image_folders:
    image_folder_path: str = f"{PORTFOLIO_DIR}/{image_folder}".rstrip("/")
    thumbnail_folder_path: str = f"{image_folder_path}/{THUMBNAIL_DIR}"
    print(thumbnail_folder_path)

    image_folder_contents = client.list(image_folder_path)[1:]
    images = [item for item in image_folder_contents if not item.endswith("/")]

    if THUMBNAIL_DIR not in image_folder_contents:
        client.mkdir(thumbnail_folder_path)
    else:
        print(f"{thumbnail_folder_path} already exists.")

    thumbnail_folder_contents = client.list(thumbnail_folder_path)[1:]

    missing_thumbnails = [image for image in image_folder_contents if image not in thumbnail_folder_contents and not image.endswith("/")]
    orphaned_thumbnails = [image for image in thumbnail_folder_contents if image in thumbnail_folder_contents and image not in image_folder_contents]

    print(f"missing_thumbnails: {missing_thumbnails}")
    print(f"orphaned_thumbnails: {orphaned_thumbnails}")

    # Delete orphaned thumbnails
    for image in orphaned_thumbnails:
        thumbnail_path: str = f"{thumbnail_folder_path}/{image}"
        image_path: str = f"{image_folder_path}/{image}"

        client.clean(thumbnail_path)
        print("Orphaned thumbnails deleted.")


    print(f"missing_thumbnails: {missing_thumbnails}")

    # Create missing thumbnails
    for image in missing_thumbnails:
        thumbnail_path: str = f"{thumbnail_folder_path}/{image}"
        image_path: str = f"{image_folder_path}/{image}"
        extension = os.path.splitext(image_path)[1]

        print(f"image_path: {image_path}")
        print(f"thumbnail_path: {thumbnail_path}")

        print(f"{extension}")

        temp_file: _TemporaryFileWrapper[bytes] = tempfile.NamedTemporaryFile(
            suffix=extension,
            delete_on_close=True
        )
        temp_path = temp_file.name
        print(f"{temp_path} path created.")
        client.download_sync(
            remote_path=image_path,
            local_path=temp_path
        )
        print(f"{image_path} downloaded to {temp_path}.")
        
        img = Image.open(temp_path)
        res = img.resize((300, 300))
        print("Image resized.")
        temp_file.close()

        temp_file: _TemporaryFileWrapper[bytes]= tempfile.NamedTemporaryFile(
            suffix=extension,
            delete_on_close=True,
        )
        temp_path = temp_file.name

        res.save(temp_path)

        client.upload_sync(remote_path=thumbnail_path, local_path=temp_path)

        temp_file.close()