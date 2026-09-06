from flask import Blueprint, render_template, send_file, send_from_directory
from .webdav import get_folders, get_folder_images, get_image

main_bp = Blueprint("main", __name__)

@main_bp.route("/favicon.ico")
def favicon():
    return send_from_directory(
        "static",
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )

@main_bp.route('/', methods=['GET'])
def index():
    folders = get_folders()
    return render_template('index.html',
    folders=folders)

@main_bp.route('/<folder>', methods=['GET', 'POST'])
def folder(folder):
    images = get_folder_images(folder)

    return render_template(
        'folder.html',
        images=images,
        folder=folder)

@main_bp.route('/<folder>/<image>')
def image(folder, image):
    local_path = get_image(folder, image)
    return send_file(
        local_path,
        mimetype="image/jpeg"
    )