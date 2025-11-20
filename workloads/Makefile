CXX = gcc
GXX = g++

FFT = fft
BUBBLESORT = bubblesort
MATMUL = matrix-multiply
HELLO = hello-gem5
OUTDIR = binaries
GEM5_PATH=/usr/local-eit/cad2/gem5/gem5/

clean:
	rm $(OUTDIR)/*.o

$(OUTDIR)/$(FFT).o: $(FFT)/$(FFT).cpp
	$(GXX) $(FFT)/$(FFT).cpp -o $(OUTDIR)/$(FFT).o \ 
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/x86/out -lm5 -static-libstdc++
	md5sum $(OUTDIR)/$(FFT).o
$(OUTDIR)/$(BUBBLESORT).o: $(BUBBLESORT)/$(BUBBLESORT).cpp
	$(GXX) $(BUBBLESORT)/$(BUBBLESORT).cpp -o $(OUTDIR)/$(BUBBLESORT).o \ 
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/x86/out -lm5 -static-libstdc++
	md5sum $(OUTDIR)/$(BUBBLESORT).o
$(OUTDIR)/$(MATMUL).o: $(MATMUL)/$(MATMUL).c
	$(CXX) $(MATMUL)/$(MATMUL).c -o $(OUTDIR)/$(MATMUL).o -I/usr/local-eit/cad2/gem5/gem5/include -L/usr/local-eit/cad2/gem5/gem5/util/m5/build/x86/out -lm5 -static-libstdc++
	md5sum $(OUTDIR)/$(MATMUL).o
$(OUTDIR)/$(HELLO).o: $(HELLO)/$(HELLO).c
	$(CXX) $(HELLO)/$(HELLO).c -o $(OUTDIR)/$(HELLO).o \ 
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/x86/out -lm5 -static-libstdc++
	md5sum $(OUTDIR)/$(HELLO).o

all: $(OUTDIR)/$(MATMUL).o $(OUTDIR)/$(BUBBLESORT).o $(OUTDIR)/$(FFT).o $(OUTDIR)/$(HELLO).o
