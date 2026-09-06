import os
from webdav3.client import Client

client = Client({
    "webdav_hostname": os.environ["WEBDAV_HOSTNAME"],
    "webdav_login": os.environ["WEBDAV_LOGIN"],
    "webdav_password": os.environ["WEBDAV_PASSWORD"],
})

PORTFOLIO_DIR = "Photos/portfolio/compressed"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
}


def get_portfolio_folders():
    items = client.list(PORTFOLIO_DIR)
    folders = []

    for item in items:
        item = item.strip("/")

        # Ignore the current directory and parent directory entries
        if item in {"", ".", ".."}:
            continue

        item_path = f"{PORTFOLIO_DIR}/{item}"

        try:
            # A directory can be listed successfully
            client.list(item_path)
            folders.append(item)
        except Exception:
            # It is probably a file
            continue

    return sorted(folders)



def get_portfolio_images(folder):
    folder_path = f"{PORTFOLIO_DIR}/{folder}"
    images = []

    for item in client.list(folder_path):
        filename = item.strip("/").split("/")[-1]
        extension = os.path.splitext(filename)[1].lower()

        if extension in IMAGE_EXTENSIONS:
            images.append({
                "name": filename,
                "path": f"{folder_path}/{filename}",
            })

    return images


def download_image(remote_path, local_path):
    client.download_sync(
        remote_path=remote_path,
        local_path=local_path,
    )
