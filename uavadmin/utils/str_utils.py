import re
import string
from difflib import SequenceMatcher

# from PyObfuscator import Obfuscator


def string_similarity(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()


def clean_string(input_string):
    # 定义可见字符集合
    printable = set(string.printable)

    # 过滤字符串中的不可见字符
    cleaned_string = "".join(filter(lambda x: x in printable, input_string))

    return cleaned_string


def remove_control_characters(s):
    return re.sub(r"[\x00-\x1F\x7F-\x9F]", "", s)


def decode_confused_string(confused_str):
    # 分割混淆字符串，获取十六进制编码列表
    hex_codes = confused_str.split("<")[1:]

    # 将十六进制编码转换为字符，并拼接成原始字符串
    original_str = "".join(chr(int(code[:4], 16)) for code in hex_codes)

    return original_str


if __name__ == "__main__":
    s = "F⁣l⁮u͏s⁡h﻿i⁬n⁯g⁫"
    print(clean_string(s))
