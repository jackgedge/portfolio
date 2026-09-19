from typing import Any
from PIL.ImageFile import ImageFile
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

image_folders: list[str] = [item for item in portfolio_list if item.endswith("/")]

# Iterate through image folders
for image_folder in image_folders:
    image_folder_path: str = f"{PORTFOLIO_DIR}/{image_folder}".rstrip("/")
    thumbnail_folder_path: str = f"{image_folder_path}/{THUMBNAIL_DIR}"
    print(thumbnail_folder_path)

    image_folder_contents = client.list(image_folder_path)[1:]
    images: list[str] = [item for item in image_folder_contents if not item.endswith("/")]

    if THUMBNAIL_DIR not in image_folder_contents:
        client.mkdir(thumbnail_folder_path)
    else:
        print(f"{thumbnail_folder_path} already exists.")

    thumbnail_folder_contents = client.list(thumbnail_folder_path)[1:]

    missing_thumbnails: list[str] = [image for image in image_folder_contents if image not in thumbnail_folder_contents and not image.endswith("/")]
    orphaned_thumbnails: list[str] = [image for image in thumbnail_folder_contents if image in thumbnail_folder_contents and image not in image_folder_contents]

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
        thumbnail_path = f"{thumbnail_folder_path}/{image}"
        image_path = f"{image_folder_path}/{image}"
        extension = os.path.splitext(image)[1].lower()

        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=True,
        ) as source_file:
            source_path: str = source_file.name

            client.download_sync(
                remote_path=image_path,
                local_path=source_path,
            )

            # Load the image while the temporary file is still open.
            with Image.open(source_path) as opened_image:
                img: Image.Image = opened_image.convert("RGB")
                img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

                # Copy the resized image so it remains usable after the context closes.
                thumbnail: Image.Image = img.copy()

        # JPEG is generally smaller for photographic thumbnails.
        with tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False,
        ) as thumbnail_file:
            thumbnail_path_local: str = thumbnail_file.name

        try:
            thumbnail.save(
                thumbnail_path_local,
                format="JPEG",
                quality=85,
                optimize=True,
                progressive=True,
            )

            client.upload_sync(
                remote_path=thumbnail_path,
                local_path=thumbnail_path_local,
            )
        finally:
            os.remove(thumbnail_path_local)