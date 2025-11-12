CXX = gcc
GXX = g++

BINSEARCH = binary-search
BUBBLESORT = bubblesort
MATMUL = matrix-multiply
HELLO = hello-gem5
OUTDIR = binaries

clean:
	rm $(OUTDIR)/*.o

$(OUTDIR)/$(BINSEARCH).o: $(BINSEARCH)/$(BINSEARCH).cpp
	$(GXX) $(BINSEARCH)/$(BINSEARCH).cpp -o $(OUTDIR)/$(BINSEARCH).o
	md5sum $(OUTDIR)/$(BINSEARCH).o
$(OUTDIR)/$(BUBBLESORT).o: $(BUBBLESORT)/$(BUBBLESORT).cpp
	$(GXX) $(BUBBLESORT)/$(BUBBLESORT).cpp -o $(OUTDIR)/$(BUBBLESORT).o
	md5sum $(OUTDIR)/$(BUBBLESORT).o
$(OUTDIR)/$(MATMUL).o: $(MATMUL)/$(MATMUL).c
	$(CXX) $(MATMUL)/$(MATMUL).c -o $(OUTDIR)/$(MATMUL).o
	md5sum $(OUTDIR)/$(MATMUL).o
$(OUTDIR)/$(HELLO).o: $(HELLO)/$(HELLO).c
	$(CXX) $(HELLO)/$(HELLO).c -o $(OUTDIR)/$(HELLO).o
	md5sum $(OUTDIR)/$(HELLO).o

all: $(OUTDIR)/$(MATMUL).o $(OUTDIR)/$(BUBBLESORT).o $(OUTDIR)/$(BINSEARCH).o $(OUTDIR)/$(HELLO).o
