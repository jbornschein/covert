CFLAGS=-O3 -DMAIN=1 #-std=gnu99

all: backend 

backend: backend.c
	gcc -g $(CFLAGS) backend.c -o backend
	gcc -g $(CFLAGS) -S backend.c

clean:
	rm -f backend backend_O2 pyback.c pyback.so


