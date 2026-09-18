from tempfile import _TemporaryFileWrapper
from flask.cli import load_dotenv
from webdav3.client import Client
from pathlib import Path
import os 
import tempfile
import random
from PIL import Image

# Define project directory and environment file location.
PROJECT_DIR: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = PROJECT_DIR / ".env"

# Load environment variables
load_dotenv(ENV_FILE)

PORTFOLIO_DIR: str | None = os.getenv('PORTFOLIO_DIR')
THUMBNAIL_DIR = ".thumbnails"

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

def clean_images(images):

    clean_images = [] 

    clean_images: list[str] = [
        image
        for image in images
        if image.lower().endswith(tuple(IMAGE_FORMATS))
    ]
    return clean_images

def get_folder_images(folder):
    folder_path: str = f"{PORTFOLIO_DIR}/{folder}"
    images = client.list(folder_path)[1:]
    
    clean_images = clean_images(images)

    return clean_images

def create_thumbnails(folder):
    folder_path: str = f"{PORTFOLIO_DIR}/{folder}"
    folder_contents = client.list(folder_path)[1:]
    thumbnail_folder_path: str = f"{PORTFOLIO_DIR}/{folder}/{THUMBNAIL_DIR}"

    if thumbnail_folder_path not in folder_contents:
        client.mkdir(thumbnail_folder_path)
        print(f"{thumbnail_folder_path} created.")
    else: 
        print(f"{thumbnail_folder_path} already exists.")

    thumbnail_folder_contents = client.list(thumbnail_folder_path)
    
    for file in folder_contents:

        file_path = f"{PORTFOLIO_DIR}/{folder}/{file}"

        thumbnail_path = f"{PORTFOLIO_DIR}/{folder}/{THUMBNAIL_DIR}/tn_{file}"

        extension = os.path.splitext(thumbnail_path)[1]

        if file not in  thumbnail_folder_contents:
            
            temp_file: _TemporaryFileWrapper[bytes] = tempfile.NamedTemporaryFile(
                suffix=extension,
                delete_on_close=True
            )
            temp_path = temp_file.name

            client.download_sync(
                remote_path=file_path,
                local_path=temp_path
            )
            
            img = Image.open(temp_path)
            res = img.resize((300, 300))
            temp_file.close()

            temp_file: _TemporaryFileWrapper[bytes]= tempfile.NamedTemporaryFile(
                suffix=extension,
                delete_on_close=True,
            )
            temp_path = temp_file.name

            res.save(temp_path)

            client.upload_sync(remote_path=thumbnail_path, local_path=temp_path)

            temp_file.close()
            




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
        min(15, len(all_images))
    )