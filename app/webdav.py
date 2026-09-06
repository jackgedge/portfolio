from flask.cli import load_dotenv
from webdav3.client import Client
import os 

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

folders = client.list(PORTFOLIO_DIR)[1:]

def get_folder_images(folder):
    folder_path = f"{PORTFOLIO_DIR}/{folder}"
    images = client.list(folder_path)
    return images