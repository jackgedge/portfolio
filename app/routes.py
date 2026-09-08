from flask import Blueprint, render_template, send_file, send_from_directory, after_this_request, url_for, redirect
from .webdav import get_folders, get_folder_images, get_image
import os

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

    #TODO Generate random selection of images from portfolio to display on home. 

    return render_template('index.html',
    folders=folders)

@main_bp.route('/<folder>', methods=['GET', 'POST'])
def folder(folder):
    folders = get_folders()
    images = get_folder_images(folder)

    return render_template(
        'folder.html',
        images=images,
        folder=folder,
        folders=folders)

@main_bp.route("/<folder>/<image>")
def image(folder, image):
    local_path = get_image(folder, image)

    @after_this_request
    def delete_temp_file(response):
        try:
            os.unlink(local_path)
        except FileNotFoundError:
            pass
        return response

    return send_file(
        local_path,
        mimetype="image/jpeg",
    )


dev_bp = Blueprint('dev', __name__)

@dev_bp.route('/broken')
def broken():
    folders = get_folders()
    return render_template(
        'broken.html',
        folders=folders
    )


social_bp = Blueprint('social', __name__)

@social_bp.route('/contact')
def contact():
    # TODO
    return redirect(url_for('dev.broken'))