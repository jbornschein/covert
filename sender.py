#!/usr/bin/env python

from __future__ import division

from time import sleep, time
import numpy as np

# 
freq = 200    # in Hz
size = 32     # in MB

# Allocate big memory
buf1 = np.empty( (size*1024*104), dtype= np.uint8)
buf2 = np.empty( (size*1024*104), dtype= np.uint8)


def send_byte(byte):
    """
        takes (1. / freq) * 8 seconds
    """
    
    bit_time = 1. / freq 

    t0 = time()
    pos = int( (time() - t0) // bit_time )
    while pos < 8:
        bit = byte & (2 << pos)
        if bit:
            buf1[:] = buf2[:]

        pos = int( (time() - t0) // bit_time )


byte = 42
sleep(2)
while True:
    send_byte(2+8+32+128)
    send_byte(0)

    #send_byte(42)
    #send_byte(2+8+32+128)
    #send_byte(byte)
    #send_byte(2+8+32+128)
    #send_byte(0)

