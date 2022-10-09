from pathlib import Path

from cloudphoto.config import get_bucket_name, is_album_exist


def download_img(session, album: str, path: str):
    path = Path(path)
    bucket = get_bucket_name()
    if not is_album_exist(session, bucket, album):
        raise Exception("Album does not exist")

    if not path.is_dir():
        raise Exception(f"{str(path)} is not directory")

    list_object = session.list_objects(Bucket=bucket, Prefix=album + '/', Delimiter='/')
    for key in list_object["Contents"]:
        obj = session.get_object(Bucket=bucket, Key=key["Key"])
        filename = Path(key['Key']).name

        filepath = path / filename
        with filepath.open("wb") as file:
            file.write(obj["Body"].read())
