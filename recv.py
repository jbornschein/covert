#!/usr/bin/env python

from __future__ import division

from time import sleep, time
import matplotlib
import numpy as np



def measure(secs=10, rate=2500):
    spls   = secs * rate
    size   = 16   # MB
    stride = 0.5  # MB
    MB     = 1024*1024
    
    # Allocate big memory
    buf1 = np.ones( (size*MB), dtype= np.uint8)
    buf2 = np.ones( (size*MB), dtype= np.uint8)

    result = np.zeros( (spls) )
    result[:] = np.nan

    delta_t = secs / spls

    t0 = time()
    cur_spl = 0
    next_time = t0 + delta_t
    time_passed = time() - t0
    i = 0
    t_mean = 0.
    while time_passed < secs:
        i = (i + 1) % (size // stride)
        rng = slice( i*stride*MB , (i+1)*stride*MB )
        t1 = time()
        buf1[rng] = buf2[rng]
        t_diff = time() - t1
        t_mean = (t_mean + t_diff) / 2
        
        offset = time_passed // delta_t 

        #print "next_time=%d offset=%d" % (next_time, offset)
        result[offset] = t_mean
        time_passed = time() - t0

    bw = stride*MB / result

    return bw


