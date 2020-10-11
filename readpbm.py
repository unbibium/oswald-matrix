#!/usr/bin/env python3

"""
This is an I/O library to read an old-fashioned portable bitmap
(PBM) file and make sure that it can be converted into a
sprite tile.
"""

import math

class PBM:
    def __init__(self, fn):
        "readpbm(fn) -> 1008 bytes of bitmap"
        with open(fn,'rb') as f:
            magicnum = (f.read(3))
            if magicnum != b'P4\n':
                raise ValueError(fn+" does not appear to be a pbm file")
            resolution = f.readline().decode("us-ascii").strip()
            w,h = map(int,resolution.split(' ',1))
            if w != 96 or h != 84:
                raise ValueError("wrong resolution: " + resolution)
            self.pbmdata = f.read(1008)
            self.w, self.h = w, h
            self.bw = math.ceil(w/8)
            self.out=0

    def segment(self, segx, segy, segw, segh):
        segbw=int(segw/8)
        resultsize = segh * segbw
        result = bytearray(math.ceil(resultsize/8)*8)
        offset = segy * segh * self.bw + segx * segbw
        for row in range(segh):
            resultoffset = row * segbw
            sourceoffset = offset + row * self.bw
            if sourceoffset+segbw < len(self.pbmdata):
                result[resultoffset:resultoffset+segbw] = self.pbmdata[sourceoffset:sourceoffset+segbw]
        self.out = self.out + len(result)
        return result

    def all_segments(self, segw, segh):
        tiles = []
        for y in range(math.ceil(self.h/segh)):
            for x in range(int(self.w/segw)):
                tiles.append(self.segment(x,y,segw,segh))
        return b''.join(tiles)

if __name__=='__main__':
    print("This is a module.")
