from flask import Blueprint, render_template
from .webdav import folders, get_folder_path, get_folder_images

main_bp = Blueprint("main", __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html',
    folders=folders)

@main_bp.route('/<folder>', methods=['GET', 'POST'])
def folder(folder):
    images = get_folder_images(folder)
    return render_template('folder.html',
    images=images)