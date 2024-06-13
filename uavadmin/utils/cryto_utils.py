import base64
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def random_string(length):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = "".join(chars[os.urandom(1)[0] % len(chars)] for _ in range(length))
    return result


def encrypt(word, keys, iv_org=None):
    key = keys.encode("utf-8")
    if not iv_org:
        iv_org = random_string(16)
    iv = iv_org.encode("utf-8")

    cipher = AES.new(key, AES.MODE_CBC, iv)
    srcs = pad(word.encode("utf-8"), AES.block_size)
    encrypted = cipher.encrypt(srcs)

    res = iv + encrypted
    return base64.b64encode(res).decode("utf-8")


if __name__ == "__main__":
    # Example usage:
    word = "hzy123"
    keys = "GVJD5Ola4s3VfeTc"  # Ensure this key is 16 bytes long
    encrypted = encrypt(word, keys, iv_org="0123456789abcdef")
    print("Encrypted:", encrypted)
