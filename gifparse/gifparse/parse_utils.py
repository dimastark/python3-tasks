#!/usr/bin/env python3
""" Parsing functions """


def parse_int(bts, order='little'):
    """ int.from_bytes alias """
    return int.from_bytes(bts, byteorder=order)


def bytes_from(file_name):
    """ Make list of bytes from file """
    with open(file_name, mode='br') as file:
        return file.read()


def get_frame_rectangle(f_bytes):
    """ Get rectangle of gif frame from bytes representation """
    x = parse_int(f_bytes[:2], 'little')
    y = parse_int(f_bytes[2:4], 'little')
    width = parse_int(f_bytes[4:6], 'little')
    height = parse_int(f_bytes[6:8], 'little')
    return x, y, width, height


def get_ct_length(f_byte):
    """ Get length of color table for gif """
    # FIXME: WTF IS THIS?!
    bin_line = bin(parse_int([f_byte], 'big'))[2:].rjust(8, "0")
    ct_flag = bool(int(bin_line[0], 2))
    return 3 * 2 ** (int(bin_line[-3:], 2) + 1) if ct_flag else 0


def parse_ct(bts):
    """Parse Color Table. Local or Global"""
    colors = []
    for i in range(0, len(bts), 3):
        color = bts[i:i + 3]
        r_part = parse_int([color[0]], 'big')
        g_part = parse_int([color[1]], 'big')
        b_part = parse_int([color[2]], 'big')
        colors.append((r_part, g_part, b_part))
    return colors
