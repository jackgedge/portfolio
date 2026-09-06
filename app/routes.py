from pathlib import PurePosixPath
import mimetypes
import os
import tempfile

from flask import Blueprint, abort, render_template, request, send_file

from .webdav_client import (
    download_image,
    get_portfolio_folders,
    get_portfolio_images,
)

main_bp = Blueprint("main", __name__)

ALLOWED_PREFIX = PurePosixPath("Photos/portfolio/compressed")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def validate_image_path(raw_path: str) -> str:
    # WebDAV paths should use POSIX separators regardless of host OS.
    path = PurePosixPath(raw_path)

    # Reject absolute paths and traversal components before normalization.
    if path.is_absolute() or ".." in path.parts:
        abort(403, description="Invalid image path")

    try:
        relative_path = path.relative_to(ALLOWED_PREFIX)
    except ValueError:
        abort(403, description="Invalid image path")

    if not relative_path.parts:
        abort(403, description="Invalid image path")

    extension = PurePosixPath(path.name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        abort(403, description="Unsupported image type")

    return path.as_posix()


@main_bp.route("/")
def portfolio():
    return render_template(
        "portfolio.html",
        folders=get_portfolio_folders(),
    )


@main_bp.route("/<folder>")
def folder(folder):
    if not folder or "/" in folder or "\\" in folder:
        abort(404)

    return render_template(
        "folder.html",
        folder=folder,
        images=get_portfolio_images(folder),
    )


@main_bp.route("/<folder>/<image>")
def image(folder, image):
    return render_template(
        "image.html",
        folder=folder,
        image=image,
    )

@main_bp.route("/portfolio-image")
def portfolio_image():
    raw_path = request.args.get("path")
    if not raw_path:
        abort(400, description="Missing image path")

    remote_path = validate_image_path(raw_path)
    extension = PurePosixPath(remote_path).suffix.lower()

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temporary_file:
            temporary_path = temporary_file.name

        download_image(
            remote_path=remote_path,
            local_path=temporary_path,
        )

        mime_type = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }[extension]

        response = send_file(
            temporary_path,
            mimetype=mime_type,
            max_age=3600,
        )

        response.call_on_close(
            lambda: (
                os.unlink(temporary_path)
                if temporary_path and os.path.exists(temporary_path)
                else None
            )
        )

        return response

    except Exception:
        if temporary_path and os.path.exists(temporary_path):
            os.unlink(temporary_path)

        abort(404, description="Image could not be downloaded")
