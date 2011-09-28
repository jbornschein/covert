CFLAGS=-DMAIN=1

all: backend backend_O2

backend: backend.c
	gcc -g $(CFLAGS) backend.c -o backend

backend_O2: backend.c
	gcc -O2 $(CFLAGS) backend.c -o backend_O2


clean:
	rm -f backend backend_O2 pyback.c pyback.so


