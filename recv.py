#!/usr/bin/env python

from __future__ import division

from time import sleep, time
import matplotlib
import pylab
import numpy as np
import pyback

from covert_fsk import Covert, show_sig


cc = Covert(bit_rate=100., f0=600., f1=900., spl_rate=50000)

while True:
    S = pyback.measure(1 * 1000 * 1000, 50000)
    S_ = cc.bandpass(S)
    B = cc.demod(S_)
    pkts = cc.decode(B)

    pylab.figure(1); 
    pylab.subplot(2,1,1); show_sig(S, 5*20*4)
    pylab.subplot(2,1,2); show_sig(B, 5*20*4)
    pylab.draw()
    
    print 78*"-"
    for p in pkts:
        if len(p) == len(cc.test_pkt):
            print "%1.4f: %s" % (np.mean(np.abs(p - cc.test_pkt)), p)

