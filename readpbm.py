#!/usr/bin/env python3

"""
This is an I/O library to read an old-fashioned portable bitmap
(PBM) file and make sure that it can be converted into a
sprite tile.
"""

def readpbm(fn):
    "readpbm(fn) -> 1008 bytes of bitmap"
    with open(fn,'rb') as f:
        magicnum = (f.read(3))
        if magicnum != b'P4\n':
            raise ValueError(fn+" does not appear to be a pbm file")
        resolution = f.readline().decode("us-ascii").strip()
        w,h = map(int,resolution.split(' ',1))
        if w != 96 or h != 84:
            raise ValueError("wrong resolution: " + resolution)
        return f.read(1008)

if __name__=='__main__':
    print("This is a module.")
