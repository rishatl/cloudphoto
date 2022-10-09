import sys

from botocore.exceptions import ClientError

from cloudphoto.config import create_config
from delete import delete_img, delete_album
from download import download_img
from list import list_albums, list_img
from upload import upload_photo

from cloudphoto.s3_session import create_s3_session, init_s3_session

DEFAULT_ENDPOINT = "https://storage.yandexcloud.net"
DEFAULT_REGION = "ru-central1"


def upload(session):
    params = {"album": None, "path": None}

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        raise Exception("Не хватает параметров")

    try:
        params[sys.argv[4][2:]] = sys.argv[5]
    except Exception as e:
        pass

    if not params.get("album"):
        raise Exception("Введите параметр album")

    if params.get("album").find("/") != -1:
        raise Exception("Параметр album не может содержать символ /")

    upload_photo(session, params.get("album"), (params.get("path") if params.get("path") else "."))


def download(session):
    params = {"album": None, "path": None}

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        raise Exception("Не хватает параметров")

    try:
        params[sys.argv[4][2:]] = sys.argv[5]
    except Exception as e:
        pass

    if not params.get("album"):
        raise Exception("Введите параметр album")

    download_img(session, params.get("album"), params.get("path"))


def list_command(session):
    params = {
        "album": None,
    }

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        pass
    list_img(session, params.get("album")) if params.get("album") else list_albums(session)


def delete(session):
    params = {"album": None, "photo": None}

    try:
        params[sys.argv[2][2:]] = sys.argv[3]
    except Exception as e:
        raise Exception("Не хватает параметров")

    try:
        params[sys.argv[4][2:]] = sys.argv[5]
    except Exception as e:
        pass

    if not params.get("album"):
        raise Exception("Введите параметр album")

    delete_img(session, params.get("album"), params.get("photo")) if params.get("photo") else delete_album(session,
                                                                                                           params.get(
                                                                                                               "album"))


def mksite(session):
    mksite(session)


def init_com():
    access_key = input("access key: ")
    secret_access_key = input("secret access key: ")
    bucket_name = input("bucket name: ")
    try:
        s3 = create_s3_session(access_key, secret_access_key, DEFAULT_ENDPOINT, DEFAULT_REGION)
        s3.create_bucket(Bucket=bucket_name, ACL='public-read-write')
    except ClientError as clientError:
        if clientError.response["Error"]["Code"] != "BucketAlreadyOwnedByYou":
            raise clientError

    create_config(access_key=access_key, secret_key=secret_access_key, bucket_name=bucket_name)


COMMANDS_NAME_AND_FUNCTIONS = {
    "upload": upload,
    "download": download,
    "list": list_command,
    "delete": delete,
    "mksite": mksite,
    "init": init_com,
}


def main():
    sys.tracebacklimit = -1

    try:
        command = sys.argv[1]
    except Exception as e:
        raise Exception("Введите команду")

    function = COMMANDS_NAME_AND_FUNCTIONS.get(command)

    if function != init_com:
        session = init_s3_session()
        function(session)
    else:
        function()


if __name__ == "__main__":
    main()
