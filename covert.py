#~/usr/bin/env python
"""

DO NOT USE -- THIS IS OLD GARBAGE!


"""




from __future__ import division

from time import sleep, time
import matplotlib
import pylab
import numpy as np

from segmentaxis import segment_axis


class CovertChannel:
    def __init__(self, rate=2000, bufstride=0.25, bufsize=16):
        MB = 1024*1024
        self.rate = rate
        self.bufstride = bufstride*MB
        self.bufsize = bufsize*MB
        self.low_cut_freq = 2.
        self.medfilt_width = 7

        # Allocate BW-measure buffer
        self.buf1 = np.ones( (self.bufsize), dtype= np.uint8)
        self.buf2 = np.ones( (self.bufsize), dtype= np.uint8)

    ######################################################################
    # Sending side
    def send_bits(self, arr):
        """
        """
        symbols = ([1,0,0,0], [1,1,1,0])

        slots = len(symbols[0])
        slot_time = 1. / freq 
        total_time = slots * slot_time

        t0 = time()
        cur_time = 0.
        bufpos = 0
        while cur_time < (total_time):
            cur_slot = int(cur_time  / slot_time)
            cur_bit  = cur_slot % slots

            if symbols[arr[cur_bit]][cur_slot]:
                rng = slice(bufpos*bufstride, (bufpos+1)*bufstride)
                bufpos = (bufpos+1) % numstrides
                buf1[rng] = buf2[rng]
            cur_time = time() - t0

    def send_buf(self, buf):
        pass

    
    def send_packet(self, data):
        bits = []
        bits += 4*[1, 0]

    ######################################################################
    # Recv. side
    def measure(self, secs=10):
        """
            Measure available bandwidth for *sec* seconds.
    
            Returns an array with sec*rate elements.
        """
        rate = self.rate
        bufsize = self.bufsize
        bufstride = self.bufstride
        numstrides = bufsize // bufstride
        
        buf1 = self.buf1
        buf2 = self.buf2

        spls = secs * rate
        delta_t = 1. / rate
    
        # Allocate return 
        copy_time = np.zeros( (spls) )
    
        i = 0
        last_offset = 0

        t0 = time()
        time_passed = time() - t0
        while time_passed < secs:
            # Determin stride of buffers to copy around..
            rng = slice(i*bufstride , (i+1)*bufstride)
            i = (i + 1) % numstrides    # for next iteration, use differend stride

            # Copy and measure
            t1 = time(); 
            buf1[rng] = buf2[rng]
            t_measure = time() - t1

            # Store measured time into result array
            offset = time_passed // delta_t 
            copy_time[last_offset:offset] = t_measure
            last_offset = offset

            # Prepare for next iteration
            time_passed = time() - t0
    
        # Fill remaining measurements (if neccessary)
        copy_time[last_offset:] = t_measure
        
        # Return actual memory bandwidth
        bw = bufstride / copy_time
        return bw
    

    def filter(self, S):
        """
            Apply filtering on the bandwidth measurements provided in S.
            Returns an array with filtered but still continuous values.
        """ 
        rate = self.rate
        garbage = rate / 200 * 16
        
        # High pass // remove DC 
        #cut_point = 2.*self.low_cut_freq / rate
        #b, a = signal.iirdesign(wp=cut_point, ws=cut_point/1.1, gstop=10, gpass=1.1, ftype='cheby1')
        #S_ = signal.lfilter(b, a, S)
        #S_ = S_[garbage:]     # throw away garbage in the beginning

        #print "cut_point", cut_point
        #print "b[:%d] = %s" % (len(b), b)
        #print "a[:%d] = %s" % (len(a), a)

        # Remove DC-part; windowed
        dc_window = 100
        sa = segment_axis(S, dc_window, dc_window-1)
        M = np.mean(sa, axis=0)
        S_ = S[:len(M)] - M

        # Remove high frequency noise using median filter
        S_ = signal.medfilt(S_, self.medfilt_width)

        # And normalize
        S_ /= S_.max()

        return S_

    def decode(self, S):
        # Find positive and negative domains
        M = 1*(S > 0)

        pos_edge = (M[:-1] - M[1:]) == -1
        neg_edge = (M[:-1] - M[1:]) == +1
        
        pos_edges = np.where(pos_edge)[0]
        neg_edges = np.where(neg_edge)[0]

        if pos_edges[0] < neg_edges[0]:
            pos_edges = pos_edges[1:]
    
        pl = len(pos_edges)
        nl = len(neg_edges)
        cl = min(pl, nl)

        length = pos_edges[:cl] - neg_edges[:cl]

        print pos_edges
        print neg_edges
        print length
        
        
        return length
