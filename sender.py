#!/usr/bin/env python 

from __future__ import division

import numpy as np

from time import sleep
from covert_fsk import Covert



if __name__ == "__main__":
    cc = Covert()

    while True:
        print "Sending..."
        cc.send_bits( cc.sync_pattern.tolist() + cc.test_pkt.tolist() )
        sleep(.5)

