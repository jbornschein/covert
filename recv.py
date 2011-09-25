#!/usr/bin/env python

from __future__ import division

from time import sleep, time
import matplotlib
import pylab
import numpy as np

from covert_fsk import Covert


cc = Covert()

while True:

    S = cc.measure(3)
    B = cc.demod(S)
    pkts = cc.decode(B)

    print 78*"-"
    for p in pkts:
        print "%1.4f: %s" % (np.mean((p - cc.test_pkt)**2), p)

