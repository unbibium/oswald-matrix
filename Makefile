DASM=dasm
C1541=c1541

all: main.prg

main.prg: main.a65 matrix.a65 headliner.a65 images.bin
	$(DASM) main.a65 -omain.prg -smain.sym

images.bin: make-bitmaps.py
	./make-bitmaps.py

clean:
	rm main.prg images.bin

