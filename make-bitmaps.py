#!/usr/bin/env python3

# generates 6 big sprite meshes, each consisting of 12 sprites

import sys

# hex digits for debugging
digits = list(map(bytes,[
        (0x3C,0x66,0x6E,0x76,0x66,0x66,0x3c,0x00),
        (0x18,0x18,0x38,0x18,0x18,0x18,0x7E,0x00),
        (0x3C,0x66,0x06,0x0C,0x30,0x60,0x7E,0x00),
        (0x3c,0x66,0x06,0x3c,0x06,0x66,0x3c,0x00),
        (0x0c,0x1c,0x3c,0x6c,0x7E,0x0c,0x0c,0x00),
        (0x7E,0x60,0x7C,0x06,0x06,0x66,0x3c,0x00),
        (0x3c,0x66,0x60,0x7c,0x66,0x66,0x3c,0x00),
        (0x7E,0x06,0x0c,0x18,0x30,0x60,0x60,0x00),
        (0x3c,0x66,0x66,0x3c,0x66,0x66,0x3c,0x00),
        (0x3c,0x66,0x66,0x3e,0x06,0x66,0x3c,0x00),
        (0x18,0x3c,0x66,0x7e,0x66,0x66,0x66,0x00),
        (0x7c,0x66,0x66,0x7c,0x66,0x66,0x7c,0x00),
        (0x3c,0x66,0x60,0x60,0x60,0x66,0x3c,0x00),
        (0x78,0x6c,0x66,0x66,0x66,0x6c,0x78,0x00),
        (0x7E,0x60,0x60,0x7C,0x60,0x60,0x7E,0x00),
        (0x7E,0x60,0x60,0x7C,0x60,0x60,0x60,0x00)
        ]))

def sprite(num):
    "returns a sprite displaying the number in hex"
    left=int(num/16) & 0x0F
    right=num & 0x0F
    if num > 256:
        raise ValueError("sprite(%d > 256)" % num)
    result = [0] * 64
    for i in range(7):
        result[i*3  ]=digits[0][i]
        result[i*3+1]=digits[left][i]
        result[i*3+2]=digits[right][i]
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
    bytewidth = int(width/8)
    result=[]
    offset=segy*21*bytewidth + segx*3
    for row in range(21):
        rowoffset = offset+row*bytewidth
        result.append(pbmdata[rowoffset:rowoffset+3])
    return b''.join(result) + b'\0' # pad out to 64 bytes
    #return printsprite(b''.join(result) + b'\0')


def pbmtosprite(fn):
    with open(fn,'rb') as f:
        magicnum = (f.read(3))
        if magicnum != b'P4\n':
            raise ValueError(fn+" does not appear to be a pbm file")
        resolution = f.readline().decode("us-ascii").strip()
        w,h = map(int,resolution.split(' ',1))
        if w != 96 or h != 84:
            raise ValueError("wrong resolution: " + resolution)
        b = f.read(1008)
        sprites = []
        for y in range(int(h/21)):
            for x in range(int(w/24)):
                sprites.append(segment(b,x,y,w))
        return b''.join(sprites)

        


#if len(sys.argv) == 0:
    with open("images.bin",'wb') as f:
        for i in range(48):
            f.write(sprite(i))

if len(sys.argv) == 1:
    scriptname = sys.argv[0]
    print("Usage: %s [filenames]  convert pbm files to sprites" % scriptname)
    print("       %s -d           create debug sprites" % scriptname)
elif len(sys.argv) == 2 and argv[1] == '-d':
    with open("images.bin",'wb') as f:
        for i in range(48):
            f.write(sprite(i))
else: # do real conversion
    with open("images.bin",'wb') as f:
        for fn in sys.argv[1:]:
            f.write(pbmtosprite(fn))

