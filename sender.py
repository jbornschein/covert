#!/usr/bin/env python

from __future__ import division

from time import sleep, time
import numpy as np

# 
freq = 400      # in Hz
MB = 1024*1024   # 1 MB
bufsize = 32*MB  
bufstride = 0.25*MB
numstrides = bufsize // bufstride

# Allocate big memory
buf1 = np.ones( (bufsize), dtype= np.uint8)
buf2 = np.ones( (bufsize), dtype= np.uint8)

def send_bit(bit):
    """
        takes (1. / freq) * 6 seconds
    """
    bufpos = 0
    slots = 6
    slot_time = 1. / freq 
    total_time = slots * slot_time

    t0 = time()
    if bit == 0:
        symbol = [1,1,1,0,0,0]
    else:
        symbol = [1,0,1,0,1,0]
    cur_time = time() - t0
    while cur_time < (total_time):
        cur_slot = int(cur_time  / slot_time)
        if symbol[cur_slot]:
            rng = slice(bufpos*bufstride, (bufpos+1)*bufstride)
            bufpos = (bufpos+1) % numstrides
            buf1[rng] = buf2[rng]
        cur_time = time() - t0

def send_byte(byte):
    byte = int(byte)
    for i in xrange(7, -1, -1):
        send_bit( byte & (2 << i) )

def send_buf(buf):
    for i in xrange(len(buf)):
        send_byte(buf[i])

def send_str(buf):
    for i in xrange(len(buf)):
        send_byte(ord(buf[i]))

byte = 42
while True:
    print "Seing message"
    send_byte(0x00)
    send_byte(0xff)
    #send_str("Fiat Lux!")
    #sleep(.5)
    #send_byte(42)
    #send_byte(2+8+32+128)
    #send_byte(byte)
    #send_byte(2+8+32+128)
    #send_byte(0)

