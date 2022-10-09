import logging
from pathlib import Path

from cloudphoto.config import check_album, get_bucket_name

IMG_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]


def is_image(file):
    return file.is_file() and file.suffix in IMG_EXTENSIONS


def upload_photo(session, album: str, path: str):
    path = Path(path)
    check_album(album)
    count = 0

    if not path.is_dir():
        raise Exception(f"{str(path)} папка не существует")

    for file in path.iterdir():
        if is_image(file):
            try:
                print(f"{file.name} картинка загружается...")
                key = f"{album}/{file.name}"
                session.upload_file(str(file), get_bucket_name(), key)
                count += 1
            except Exception as ex:
                logging.warning(ex)

    if not count:
        raise Exception(f"В указанной папке нет изображений с расширениями, разрешенных: {IMG_EXTENSIONS}")
