
all: pyback.so

pyback.so: backend.c pyback.pyx
	cython pyback.pyx
	python setup.py build_ext --inplace

backend: backend.c
	gcc -g backend.c -o backend

backend_O2: backend.c
	gcc -O2 backend.c -o backend_O2


clean:
	rm -f backend backend_O2 pyback.c pyback.so


