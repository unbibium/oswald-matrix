Matrix Rain Plus Oswald
-----------------------

In the before-times, I had a little demo loop running on a Commodore 64
in a hackerspace.  One day we were having an open house during one of
downtown Mesa's many street festivals, and I decided to introduce a new
feature to it.

I had recently scanned some images of Oswald the Lucky Rabbit to create
some stencils in our laser cutter.  I decided to scale them down to
low-resolution bitmaps so that I could use them as a background for
the Matrix effect.  I would have to use raster interrupts to make them
cover the whole screen, even at double size.

At first I couldn't integrate it with the BASIC program I originally had
running, because I couldn't figure out how to undo all the changes I
made to the interrupts, and it couldn't return to BASIC.  Eventually
I found the KERNAL routines to reset them.

I've been tinkering with it and experimenting with DASM ever since.

Build instructions
==================

Requires `dasm`, `python3` and `make`.

Run `make` and it will create the following files:

* `oswwald-matrix.prg`: a standard demo that runs as a BASIC program.
* `comp.prg`: A standard demo that runs with SYS 12288.
* `matrix-49152.prg`: some ML routines designed for BASIC integration.

I've attached a BASIC program `cpunk.prg` which will use `matrix-49152.prg`
to both run the Matrix animation, and draw large text.

BASIC integration version
=========================

You can load this into your BASIC program the usual way.

    10 IF A=0 THEN A=1:LOAD "MATRIX-49152",8,1

You will note that the included `cpunk.prg` demo uses PEEKs instead.
This is a holdover from when I was developing on a real c64 and didn't
want to deal with reloading constantly.

If you load it into immediate mode, remember to type `NEW` so that
you don't get `?OUT OF MEMORY  ERROR`.

    SYS 49152,999,3

The second number is the number of iterations before it quits.
The third number is the picture number (0 through 3).

This build also includes a version of the Screen Headliner program,
from Compute's Gazette around 1985.  It allows you to display large
text on the screen with PETSCII.  I fixed a bug so that you can
use the entire width of the screen, up to 10 characters.  The 
original version passed parameters with POKEs, and would output only 
one character at a time, so I added some BASIC parsing to allow you 
to call it like this:

    SYS 50000,4,"HEADLINE"

The number at the end is the starting X position at the cursor.
The range is 0 to 36, so you can center a 9-character string
like this:

    SYS 50000,2,"CYBERPUNK"

Notes
=====

The empty space in `oswald-matrix.prg` is necessary because the
VIC-II chip cannot read sprite data between `$1000` and `$2000`;
it can only read the character set ROM.

I wanted to upload this to Afterlife, but I didn't want to include
all that empty space.  Downloading even at 9600 baud is slow over
the Internet due to latency, and CCGMS displays all the bytes, so
everyone would see all that blank space.  I've downloaded
uncompressed files and felt that frustration, and I didn't want to
cause it in anyone else, even if it's just 41 blocks. So I decided 
to try compacting it.

I tried BYG Compactor and a few others I was familiar with from
back in the day.  I figured I'd put the 2061 address in and it
would just run like normal.  Or maybe the BASIC RUN command.
None of these worked.

So I wrote `compactable.a65` which had no empty space but started
with SYS 12288.  I thought I could compact that and set `$3000`
as the start.  This worked when I specified "SEI" instead of "CLI"
to the compactor.  I figured this out too late to upload it to
Afterlife, though.

Another known issue is that it seems that randomly the sprites 
glitch out and flicker the wrong graphics.  I have no idea.
