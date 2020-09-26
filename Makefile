DASM=dasm
PBMS=oswald1.pbm oswald2.pbm oswald3.pbm oswald4.pbm

all: matrix-49152.prg oswald-matrix.prg compactable.prg

# oswald-matrix that can be controlled from BASIC
# and includes Screen Headliner
matrix-49152.prg: main.a65 matrix.a65 headliner.a65 images.bin
	$(DASM) main.a65 -omatrix-49152.prg -smatrix-49152.sym -lmatrix-49152.lst

# stand-alone demo
oswald-matrix.prg: sysprg.a65 mlloop.a65 matrix.a65 images.bin
	$(DASM) sysprg.a65 -ooswald-matrix.prg -soswald-matrix.sym -loswald-matrix.lst

compactable.prg: compactable.a65 mlloop.a65 matrix.a65 images.bin
	$(DASM) compactable.a65 -ocomp.prg -scomp.sym -lcomp.lst

images.bin: make-sprites.py $(PBMS)
	./make-sprites.py ${PBMS}

clean:
	rm comp.prg matrix-49152.prg images.bin oswald-matrix.prg *.sym *.lst

