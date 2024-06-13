import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from oss2.models import BucketCors, CorsRule

from appuav.settings import OSS_CONF


def list(
    folder: str = "literature",
    endpoint: str = OSS_CONF["ENDPOINT"],
    bucket: str = OSS_CONF["BUCKET"],
):
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(auth, endpoint, bucket)
    files = []
    for obj in oss2.ObjectIteratorV2(
        bucket,
        prefix=f"{folder}/",
        delimiter="/",
        start_after=f"{folder}/",
        fetch_owner=True,
    ):
        if obj.is_prefix():  # 判断obj为文件夹。
            print("directory: " + obj.key)
        else:  # 判断obj为文件。
            files.append(obj.key)
            print(f"file={obj.key} owner={obj.owner.display_name}({obj.owner.id})")
    return files


def get_download_url(
    object_name: str,
    endpoint: str = OSS_CONF["ENDPOINT"],
    bucket: str = OSS_CONF["BUCKET"],
    timeout=3600,
):
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    oss2_bucket = oss2.Bucket(auth, endpoint, bucket)

    # 解决跨域问题
    rule = CorsRule(
        allowed_origins=["*"],
        allowed_methods=["GET", "HEAD"],
        allowed_headers=["*"],
        max_age_seconds=timeout,
    )
    # 已存在的规则将被覆盖。
    oss2_bucket.put_bucket_cors(BucketCors([rule]))

    return oss2_bucket.sign_url(
        "GET",
        key=object_name,
        expires=timeout,
        slash_safe=True,
        headers=dict(),
        params=dict(),
    )


def get_full_url(
    file_name: str,
    endpoint: str = OSS_CONF["ENDPOINT"],
    bucket: str = OSS_CONF["BUCKET"],
):
    return f"https://{bucket}.{endpoint}/{file_name}"


def upload(
    path_file: str,
    file_name: str,
    endpoint: str = OSS_CONF["ENDPOINT"],
    bucket: str = OSS_CONF["BUCKET"],
):
    with open(path_file, "rb") as fileobj:
        return upload_object(fileobj, file_name, endpoint=endpoint, bucket=bucket)
    return None


def upload_object(
    fileobj,
    file_name: str,
    endpoint: str = OSS_CONF["ENDPOINT"],
    bucket: str = OSS_CONF["BUCKET"],
):
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    oss2_bucket = oss2.Bucket(auth, endpoint, bucket)
    try:
        oss2_bucket.put_object(file_name, fileobj)
        url = file_name  # f"https://{bucket}.{endpoint}/{file_name}"
        return url
    except Exception as e:
        print(f"ERROR OSS2 {e}")
    return None


def delete(
    file_name: str,
    endpoint: str = OSS_CONF["ENDPOINT"],
    bucket: str = OSS_CONF["BUCKET"],
):
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    oss2_bucket = oss2.Bucket(auth, endpoint, bucket)
    result = oss2_bucket.delete_object(file_name)
    return result
