#!/usr/bin/env python

from __future__ import division

from time import sleep, time
import matplotlib
import numpy as np



def measure(secs=10, rate=2000):
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
    last_offset = 0
    while time_passed < secs:
        i = (i + 1) % (size // stride)
        rng = slice( i*stride*MB , (i+1)*stride*MB )
        t1 = time()
        buf1[rng] = buf2[rng]
        t_diff = time() - t1
        t_mean = (t_mean + t_diff) / 2
        
        offset = time_passed // delta_t 

        result[last_offset:offset] = t_mean
        last_offset = offset
        time_passed = time() - t0

    result[last_offset:] = t_diff

    bw = stride*MB / result

    return bw

def filter_dc(signal, freq=200, rate=2000):
    length = int(rate // (freq * 2))

    N = signal.size
    #N_ = int(N // length
    filtered = np.zeros(N // length)
        
    for n in xrange(N // length):
        first = n*length
        last = first + length

        first_dc = first
        last_dc = first + 25*length

        filtered[n] = np.median(signal[first:last]) - np.mean(signal[first_dc:last_dc])

    return filtered


def filter(signal, freq=200, rate=2000):
    length = int(rate // (freq * 2))

    N = signal.size
    #N_ = int(N // length
    filtered = np.zeros(N // length)
        
    for n in xrange(N // length):
        first = n*length
        last = first + length

        filtered[n] = np.median(signal[first:last])

    return filtered




def run(secs=10, bps=0.5):
    t0 = time()

    N = 10
    bins = np.zeros( (secs*bps, N) ) 
    
    t = 0
    while time() < t0 + secs:
        S = measure(1/bps)
        S_ = np.fft.fft(S)
            
        bins[t,:]  = np.abs(S_[980:990])
        t += 1

    return bins
        
