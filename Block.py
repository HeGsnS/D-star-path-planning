#!/usr/bin/env python3
#__*__ coding: utf-8 __*__

class Block:
    def __init__(self, loc_buf):
        self.loc_buf = loc_buf
        self.dir = 0
        self.new_black_buf = []
        self.new_white_buf = []
        return

    def move(self):
        if self.loc_buf[0][1] == 0:
            self.dir = 0
        elif self.loc_buf[-1][1] == 23:
            self.dir = 1
        if self.dir == 0:
            self.loc_buf = [[x[0], x[1] + 1] for x in self.loc_buf]
        else:
            self.loc_buf = [[x[0], x[1] - 1] for x in self.loc_buf]

    def new_block_capture(self):
        if self.dir == 0:
            new_blank = self.loc_buf[0]
            new_block = self.loc_buf[-1]
        else:
            new_blank = self.loc_buf[-1]
            new_block = self.loc_buf[0]

        if new_blank in self.new_black_buf:
            self.new_black_buf.remove(new_blank)
        self.new_white_buf.append(new_blank)

        if new_block in self.new_white_buf:
            self.new_white_buf.remove(new_block)
        self.new_black_buf.append(new_block)

        return

    def __loc_buf__(self):
        return self.loc_buf

    def __new_black_buf__(self):
        return self.new_black_buf

    def __new_white_buf__(self):
        return self.new_white_buf

    def clear_history(self):
        self.new_black_buf.clear()
        self.new_white_buf.clear()
        return