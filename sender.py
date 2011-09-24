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


def send_bit(bit):
    """
        takes (1. / freq) * 8 seconds
    """
    slots = 6
    slot_time = 1. / freq 
    total_time = slots * slot_time

    t0 = time()
    if bit == 0:
        symbol = [1,0,0,0,0,0]
    else:
        symbol = [1,1,1,1,1,0]
    cur_time = time() - t0
    while cur_time < (total_time):
        cur_slot = int(cur_time  / slot_time)
        if symbol[cur_slot]:
            buf1[:] = buf2[:]
        cur_time = time() - t0

byte = 42
while True:
    send_bit(0);
    send_bit(1);
    send_bit(1);
    send_bit(1);
    send_bit(0);
    send_bit(1);
    #send_byte(42)
    #send_byte(2+8+32+128)
    #send_byte(byte)
    #send_byte(2+8+32+128)
    #send_byte(0)

