CXX = gcc
GXX = g++

FFT = fft
BUBBLESORT = bubblesort
MATMUL = matrix-multiply
HELLO = hello-gem5
OUTDIR = binaries
GEM5_PATH=PATH_TO_GEM5
FLAGS = -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/x86/out -lm5 -static-libstdc++
clean:
	rm $(OUTDIR)/*.o

$(OUTDIR)/$(FFT).o: $(FFT)/$(FFT).cpp
	$(GXX) $(FFT)/$(FFT).cpp -o $(OUTDIR)/$(FFT).o $(FLAGS)
	md5sum $(OUTDIR)/$(FFT).o
$(OUTDIR)/$(BUBBLESORT).o: $(BUBBLESORT)/$(BUBBLESORT).cpp
	$(GXX) $(BUBBLESORT)/$(BUBBLESORT).cpp -o $(OUTDIR)/$(BUBBLESORT).o $(FLAGS)
	md5sum $(OUTDIR)/$(BUBBLESORT).o
$(OUTDIR)/$(MATMUL).o: $(MATMUL)/$(MATMUL).c
	$(CXX) $(MATMUL)/$(MATMUL).c -o $(OUTDIR)/$(MATMUL).o $(FLAGS)
	md5sum $(OUTDIR)/$(MATMUL).o
$(OUTDIR)/$(HELLO).o: $(HELLO)/$(HELLO).c
	$(CXX) $(HELLO)/$(HELLO).c -o $(OUTDIR)/$(HELLO).o $(FLAGS)
	md5sum $(OUTDIR)/$(HELLO).o

all: $(OUTDIR)/$(MATMUL).o $(OUTDIR)/$(BUBBLESORT).o $(OUTDIR)/$(FFT).o $(OUTDIR)/$(HELLO).o
