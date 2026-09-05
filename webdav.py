from webdav3.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Define client options
options = {
    'webdav_hostname': os.getenv("WEBDAV_HOSTNAME"),
    'webdav_login': os.getenv("WEBDAV_LOGIN"),
    'webdav_password': os.getenv("WEBDAV_PASSWORD")
}

# Initialise client
client = Client(options)

# Define portfolio directory
portfolio_dir = "Photos/portfolio/compressed"

# Check Photos directory exists 
try:
    client.check(portfolio_dir)
    print(f"{portfolio_dir} exists.")
except:
    print(f"{portfolio_dir} does not exist.")

test_folder = '/'.join((portfolio_dir, 'japan'))

# Check test folder exists.
try:
    client.check(test_folder)
except:
    print(f"{test_folder} does not exist.")

download_path = os.path.join("./cache", 'japan')

client.download(remote_path=test_folder, local_path=download_path)