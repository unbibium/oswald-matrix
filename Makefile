DASM=dasm
PBMS=oswald1.pbm oswald2.pbm oswald3.pbm

all: main.prg

main.prg: main.a65 matrix.a65 headliner.a65 images.bin
	$(DASM) main.a65 -omain.prg -smain.sym

images.bin: make-bitmaps.py
	./make-bitmaps.py ${PBMS}

clean:
	rm main.prg images.bin

