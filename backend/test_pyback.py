#!/usr/bin/env python

import numpy as np
import pylab
import pyback


def show_sig(S, rowsize=120):
    rows = int(S.size // rowsize)
    N = rows * rowsize

    S = S[0:N].reshape( (rows, rowsize) )
    pylab.imshow(S, interpolation="nearest")


M = 1000*1000
usec = 1*M
rate = 20000
blk_size = 64*1024


while True:
    bw = pyback.measure(usec, rate, blk_size)
    show_sig(bw, rate/100)
    pylab.draw()

