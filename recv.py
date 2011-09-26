#!/usr/bin/env python

from __future__ import division

from time import sleep, time
import matplotlib
import pylab
import numpy as np

from covert_fsk import Covert, show_sig


cc = Covert()

while True:

    S = cc.measure(3)
    B = cc.demod(S)
    pkts = cc.decode(B)

    pylab.figure(1); 
    pylab.subplot(2,1,1); show_sig(S, 5*20)
    pylab.subplot(2,1,2); show_sig(B, 5*20)
    pylab.draw()
    
    print 78*"-"
    for p in pkts:
        if len(p) == len(cc.test_pkt):
            print "%1.4f: %s" % (np.mean(np.abs(p - cc.test_pkt)), p)

