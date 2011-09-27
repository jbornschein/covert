import numpy as np
cimport numpy as np

cdef extern from "backend.c":
    void  measure_c(unsigned long usec, unsigned long rate, double *bw)


def measure(sec, rate):
    N = sec = rate
    bw = np.zeros(N)

    cdef unsigned long usec = sec * 1000000
    cdef unsigned long rate_c = rate
    #cdef double *p = <double *>bw.data
    cdef np.ndarray[np.double_t,ndim=1] p = np.zeros( (N,), dtype=np.double)

    measure_c(usec, rate, <double *>p.data)

    return bw

