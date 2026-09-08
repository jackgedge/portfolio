from flask.cli import load_dotenv
from webdav3.client import Client
from pathlib import Path
import os 
import tempfile
import random

# Define project directory and environment file location.
PROJECT_DIR: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = PROJECT_DIR / ".env"

# Load environment variables
load_dotenv(ENV_FILE)

PORTFOLIO_DIR: str | None = os.getenv('PORTFOLIO_DIR')

IMAGE_FORMATS: list[str] = [
    ".jpg",
    ".jpeg",
    ]


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


def get_folder_images(folder):
    folder_path: str = f"{PORTFOLIO_DIR}/{folder}"
    images = client.list(folder_path)[1:]
    
    clean_images = []

    clean_images: list[Unknown] = [
        image
        for image in images
        if image.lower().endswith(tuple(IMAGE_FORMATS))
    ]

    return clean_images



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


def get_random_images():
    folders = client.list(PORTFOLIO_DIR)[1:]
    all_images = []

    for raw_folder in folders:
        folder = raw_folder.strip("/")

        folder_path = (
            f"{PORTFOLIO_DIR.rstrip('/')}/"
            f"{folder}"
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
        min(8, len(all_images))
    )