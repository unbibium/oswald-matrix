#!/usr/bin/env python3

# generates some big sprite meshes, each consisting of 12 sprites

import sys
import argparse

from readpbm import readpbm

# hex digits for debugging
digits = list(map(bytes.fromhex,[
        "3C666E7666663c",
        "1818381818187E",
        "3C66060C30607E",
        "3c66063c06663c",
        "0c1c3c6c7E0c0c",
        "7E607C0606663c",
        "3c66607c66663c",
        "7E060c18306060",
        "3c66663c66663c",
        "3c66663e06663c",
        "183c667e666666",
        "7c66667c66667c",
        "3c66606060663c",
        "786c6666666c78",
        "7E60607C60607E",
        "7E60607C606060"
        ]))

def hexSprite(num):
    "hexSprite(num) -> 64-byte object for a sprite displaying num in hex"
    left=int(num/16) & 0x0F
    right=num & 0x0F
    if num > 256:
        raise ValueError("hexSprite(%d > 256)" % num)
    result = [0] * 64
    for i in range(7):
        result[i*3  ]=digits[0][i]
        result[i*3+1]=digits[left][i]
        result[i*3+2]=digits[right][i]
	# checkerboard pattern at bottom
        result[62-i*3] = 85 << (i&1)
    return bytes(result)

def printsprite(data):
    if type(data) != bytes:
        raise ValueError("expected bytes, was %s" % type(data))
    if len(data) != 64:
        raise ValueError("expected 64 bytes, was %d" % len(data))
    for i in range(0,63,3):
        print("{:3d}:".format(i), end='')
        print("{:8b}{:8b}{:8b}".format(data[i],data[i+1],data[i+2]).replace('0',' '))
    return data

def segment(pbmdata,segx,segy,width):
    "segment(pbmdata,segx,segy,width) -> 64-byte object representing a chunk of the PBM data."
    bytewidth = int(width/8)
    result=[]
    offset=segy*21*bytewidth + segx*3
    for row in range(21):
        rowoffset = offset+row*bytewidth
        result.append(pbmdata[rowoffset:rowoffset+3])
    if args.print: 
        return printsprite(b''.join(result) + b'\0')
    return b''.join(result) + b'\0' # pad out to 64 bytes


def pbmtosprite(fn):
    "pbmtosprite(filename) -> bytes object with C64-compatible sprites"
    b = readpbm(fn)
    sprites = []
    h,w=84,96
    for y in range(int(h/21)):
        for x in range(int(w/24)):
            sprites.append(segment(b,x,y,w))
    return b''.join(sprites)

parser = argparse.ArgumentParser()
parser.add_argument("--numbers", type=int, help="output n sprites containing index numbers in hex")
parser.add_argument("--print", action="store_true", help="print sprites graphically to stdout")
parser.add_argument("--output", help="output filename", default="images.bin")
parser.add_argument("pbmfile", nargs="*", type=str, help="input filenames")
args = parser.parse_args()

if args.pbmfile:
    with open(args.output,'wb') as f:
        for fn in args.pbmfile:
            f.write(pbmtosprite(fn))
elif args.numbers:
    with open(args.output,'wb') as f:
        for i in range(args.numbers):
            f.write(hexSprite(i))
else:
    parser.print_usage()
    sys.exit()

