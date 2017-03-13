#!/usr/bin/env python3
""" GIF Parser by dimastark """

from gifparse.parse_utils import (
    parse_int, bytes_from, get_frame_rectangle,
    get_ct_length, parse_ct
)


class FrameInfo:
    """
    LS - Logical screen
    CT - Color Table (L - local, G - global)
    ----------------------------------------------
    | field    | type  | content                 |
    ----------------------------------------------
    | x        | int   | x and y coordinates     |
    --------------------                         |
    | y        | int   | of frame on LS          |
    ----------------------------------------------
    | colors   | list  | list of colors (r, g, b)|
    ----------------------------------------------
    | width    | int   | frame width             |
    ----------------------------------------------
    | height   | int   | frame height            |
    ----------------------------------------------
    | ct_flag  | bool  | exsistance frame LCT    |
    ----------------------------------------------
    | ct_len   | int   | Length of LCT           |
    ----------------------------------------------
    | delay    | float | Frame delay             |
    ----------------------------------------------
    """

    def __init__(self, f_bytes, delay=0.07):
        self.x, self.y, self.width, self.height = get_frame_rectangle(f_bytes[:8])
        self.ct_length = get_ct_length(f_bytes[8])
        self.colors = parse_ct(f_bytes[9:9 + self.ct_length])
        self.delay = delay

    def to_str(self):
        return '''---------------------------------
                  Place on logic screen: x={}, y={}
                  Size: width={}, height={}
                  Local colors: {}
                  Delay: {}
                  ---------------------------------'''.format(
            self.x, self.y,
            self.width, self.height,
            self.colors,
            self.delay,
        )


class GifInfo:
    # FIXME: fix this ugly class
    """
    LS - Logical screen
    CT - Color Table (L - local, G - global)
    ----------------------------------------------
    | field    | type  | content                 |
    ----------------------------------------------
    | x        | int   | x and y coordinates     |
    --------------------                         |
    | y        | int   | of Gif on LS            |
    ----------------------------------------------
    | colors   | list  | list of colors (r, g, b)|
    ----------------------------------------------
    | width    | int   | gif width               |
    ----------------------------------------------
    | height   | int   | gif height              |
    ----------------------------------------------
    | ct_flag  | bool  | exsistance  GCT         |
    ----------------------------------------------
    | ct_len   | int   | Length of GCT           |
    ----------------------------------------------
    | frames   | list  | list of FrameInfo       |
    ----------------------------------------------
    | g_ext    | list  | Graphic Extension       |
    ----------------------------------------------
    | comments | list  | List of comments        |
    ----------------------------------------------
    """

    def __init__(self, file_name):
        """Initialization from file_name"""
        self.name = file_name
        self.ind_loops = -1
        self.frames = []
        self.loops = None
        self.comments = []
        self.g_ext = []
        try:
            self.b_form = bytes_from(file_name)
            self.parse_lsd(self.b_form[:13])
            self._ip = 13
            self.colors = parse_ct(self.next_bytes(self.ct_len))
            self.parse_frames()
        except IndexError:
            raise ValueError("Unexcepted end of file")
        except Exception:
            raise
        if not self.loops:
            self.loops = 1

    def __str__(self):
        st_inf = "Name: " + self.name + '\n' + "Frames count: " + str(len(self.frames)) + '\n'
        st_inf += "Colors: " + str(self.colors) + '\n'
        st_inf += "Comments: " + str(self.comments) + '\n'
        i = 1
        st_inf += "About frames: \n"
        for frame in self.frames:
            st_inf += str(i) + ": " + '\n' + frame.to_str()
            i += 1
        return st_inf

    def parse_lsd(self, byte_arr):
        """Parse Logical Screen Descriptor"""
        data = byte_arr[:6]
        self.spec = data.decode('utf-8')
        if not self.spec.startswith("GIF"):
            raise ValueError("Wrong gif format")
        width = parse_int(byte_arr[6:8], 'little')
        height = parse_int(byte_arr[8:10], 'little')
        self.size = width, height
        self._parse_bin(byte_arr[10])
        self.num_bg_color = 0 if self.ct_flag else parse_int([byte_arr[11]], 'big')
        par = parse_int([byte_arr[12]], 'big')
        self.aratio = (par + 15) / 64 if par != 0 else 0

    def _parse_bin(self, byte):
        """Parse some special for gif binary string"""
        bin_line = bin(parse_int([byte], 'big'))[2:].rjust(8, "0")
        self.ct_flag = bool(int(bin_line[0], 2))
        self.ct_len = 3 * 2**(int(bin_line[-3:], 2) + 1) if self.ct_flag else 0
        self.colors_count = 2**(3 * (int(bin_line[1:4], 2) + 1))

    def next_byte(self):
        """Get next byte and increase ip"""
        return self.next_bytes(1)

    def next_bytes(self, count):
        """Get 'count' bytes and increase ip"""
        bts = self.b_form[self._ip:self._ip + count]
        self._ip += count
        return bts

    def parse_frame(self):
        """Parse frame bytes"""
        try:
            bts = self.b_form[self._ip:self._ip+9]
            self.frames.append(FrameInfo(bts))
            self._ip += 9 + self.frames[-1].ct_length
            self.next_byte()
            self.skip()
        except:
            raise ValueError("Corrupt frames of gif")

    def parse_gce(self):
        """Parse Graphic Control Extension"""
        length = parse_int(self.next_byte(), 'big')
        bts = self.next_bytes(length)
        delay = parse_int(bts[2:], 'little')
        bg_ind = parse_int(bts[-1:], 'big')
        self.next_byte()
        return delay, bg_ind

    def parse_ce(self):
        """Parse Comment Extension"""
        length = self.next_byte()
        comment = ""
        while length != b"\x00" and length:
            block = self.next_bytes(parse_int(length, 'big'))
            comment += block.decode("utf-8", errors='ignore')
            length = self.next_byte()
        return comment

    def parse_ne(self):
        """Parse Netscape Extension"""
        length = parse_int(self.next_byte(), 'big')
        bts = self.next_bytes(length)
        self.ind_loops = self._ip - length
        loops = parse_int(bts[-2:], 'big')
        self.loops = "Infinity" if loops == 0 else str(loops)
        self.next_byte()

    def skip(self):
        """Skip not interesting block"""
        length = self.next_byte()
        while length != b"\x00" and length:
            self.next_bytes(parse_int(length, 'big'))
            length = self.next_byte()

    def parse_frames(self):
        """Parse all frames of gif"""
        done = False
        self._ip = 13 + self.ct_len
        while not done:
            code = self.next_byte()
            if not code:
                raise ValueError("Unexcepted end of file")
            if code == b"\x2C":
                self.parse_frame()
            elif code == b"\x21":
                code = self.next_byte()
                if code == b"\xF9":
                    self.g_ext.append(self.parse_gce())
                elif code == b"\xFF":
                    self.next_byte()
                    app = self.next_bytes(11)
                    if app == b"NETSCAPE2.0":
                        self.parse_ne()
                    else:
                        self.skip()
                elif code == b"\xFE":
                    self.comments.append(self.parse_ce())
                else:
                    self.next_bytes(13)
                    self.skip()
            elif code == b"\x3B":
                done = True

    @staticmethod
    def try_parse(file_name):
        """ Try parse gif """
        try:
            return GifInfo(file_name)
        except ValueError:
            return None
