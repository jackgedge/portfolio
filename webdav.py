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

resources = client.resource(portfolio_dir)

return client, resources