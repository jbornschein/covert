import numpy as np
cimport numpy as np

cdef extern from "backend.c":
    void  measure_c(unsigned long usec, unsigned long rate, unsigned long blk_size, double *bw)


def measure(usec, rate, blk_size=65536):
    N = int(usec*rate/1000000)

    cdef unsigned long usec_c = usec
    cdef unsigned long rate_c = rate
    cdef unsigned long blk_size_c = blk_size
    #cdef double *p = <double *>bw.data
    cdef np.ndarray[np.double_t,ndim=1] p = np.zeros( (N,), dtype=np.double)

    measure_c(usec_c, rate_c, blk_size_c, <double *>p.data)

    return p

