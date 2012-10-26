# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import sys
import struct
import array

try:
    unichr = unichr
except NameError:
    unichr = chr

def unpack(fmt, data):
    fmt = str(">" + fmt)
    return struct.unpack(fmt, data)

def read_fmt(fmt, fp):
    """
    Reads data from ``fp`` according to ``fmt``.
    """
    fmt = str(">" + fmt)
    fmt_size = struct.calcsize(fmt)
    data = fp.read(fmt_size)
    assert len(data) == fmt_size, (len(data), fmt_size)
    return struct.unpack(fmt, data)

def pad(number, divisor):
    if number % divisor:
        number = (number // divisor + 1) * divisor
    return number

def read_pascal_string(fp, encoding, padding=1):
    length = read_fmt("B", fp)[0]

    if length == 0:
        fp.seek(padding-1, 1)
        return ''

    res = fp.read(length)

    fp.seek(pad(length, padding) - length, 1)
    return res.decode(encoding, 'replace')

def read_unicode_string(fp):
    num_chars = read_fmt("I", fp)[0]
    data = fp.read(num_chars*2)
    chars = be_array_from_bytes("H", data)
    return "".join(unichr(num) for num in chars)

def read_be_array(fmt, count, fp):
    """
    Reads an array from a file with big-endian data.
    """
    arr = array.array(str(fmt))
    arr.fromfile(fp, count)
    if sys.byteorder == 'little':
        arr.byteswap()
    return arr

def be_array_from_bytes(fmt, data):
    """
    Reads an array from bytestring with big-endian data.
    """
    arr = array.array(str(fmt), data)
    if sys.byteorder == 'little':
        arr.byteswap()
    return arr


def trimmed_repr(data, trim_length=30):
    if isinstance(data, bytes):
        if len(data) > trim_length:
            return repr(data[:trim_length] + b' ... =' + str(len(data)).encode('ascii'))
    return repr(data)