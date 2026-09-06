from flask.cli import load_dotenv
from webdav3.client import Client
import os 
import tempfile

load_dotenv()

hostname: str | None = os.getenv('WEBDAV_HOSTNAME')
login: str | None = os.getenv('WEBDAV_LOGIN')
password: str | None = os.getenv('WEBDAV_PASSWORD')

options: dict[str | None, str | None] = {
    'webdav_hostname': hostname,
    'webdav_login': login,
    'webdav_password': password
}

client = Client(options)

PORTFOLIO_DIR: str | None = os.getenv('PORTFOLIO_DIR')

def get_folders():
    folders = client.list(PORTFOLIO_DIR)[1:]
    folders_clean = []
    for folder_name in folders:
        folders_clean.append(folder_name.strip('/'))
    return folders_clean

def get_folder_images(folder):
    folder_path = f"{PORTFOLIO_DIR}/{folder}"
    images = client.list(folder_path)
    return images

def get_image(folder, image):
    remote_path = f"{PORTFOLIO_DIR}/{folder}/{image}".replace('//', '/')
    extension = os.path.splitext(image)[1]
    temp_file = tempfile.NamedTemporaryFile(
        suffix=extension,
        delete=False
    )
    temp_file.close()

    client.download_sync(
        remote_path=remote_path,
        local_path=temp_file.name
    )

    return temp_file.name