# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   encrypt
# @Time:    2019-06-07 12:11:53

import re
import time
import random
import base64
import hashlib
import binascii

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False


def get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ('%s%s%s' % (random.getstate(), time.time(), "")).encode()
            ).digest()
        )
    return ''.join(random.choice(allowed_chars) for i in range(length))


def get_random_secret_key():
    """
    返回长度为50的随机字符串，作为文件的SECRET_KEY
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def md5_encrypt(plaintext, salt='SmokedInk'):
    """MD5加密(64位哈希值)"""
    chaos = plaintext + salt
    md = hashlib.md5()  # 构造一个md5对象
    md.update(chaos.encode())
    cipher = md.hexdigest()
    return cipher


def md5_16_encrypt(plaintext, salt='SmokedInk'):
    """MD5加密(16位哈希值)"""
    chaos = plaintext + salt
    md = hashlib.md5()  # 构造一个md5对象
    md.update(chaos.encode())
    cipher = md.hexdigest()
    return cipher[8:-8]


def base64encrypt(content):
    """base64加密"""
    b_content = content.encode("utf-8")
    b_base64_content = base64.encodebytes(b_content)
    base64_content = b_base64_content.decode("utf-8")
    return base64_content


def base64decrypt(content):
    """base64解密"""
    b_base64_content = content.encode("utf-8")
    b_content = base64.decodebytes(b_base64_content)
    origin_text = b_content.decode("utf-8")
    return origin_text


def remove_punctuation(text, punctuation='，！？：;。“”‘’、,!?:;."\"\'`',extend_str=""):
    """去除文本标点符号"""
    punctuation = punctuation + extend_str
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text.strip()


def random_str(random_length=8):
    """随机生成指定长度字符串"""
    result_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    random_obj = random.Random()
    for i in range(random_length):
        result_str += chars[random_obj.randint(0, length)]
    return result_str


def sha1(plaintext, salt="SmokedInk"):
    """sha1加密"""
    chaos = plaintext + salt
    sha = hashlib.sha1()
    sha.update(chaos.encode())
    cipher = sha.hexdigest()
    return cipher


def crc32(content):
    """CRC32加密"""
    cipher = binascii.crc32(content)
    return '%x' % (cipher & 0xffffffff)  # 取crc32的八位数据 %x返回16进制
