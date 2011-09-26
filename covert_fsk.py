#~/usr/bin/env python

from __future__ import division

from time import sleep, time
import matplotlib
import pylab
import numpy as np
from math import pi

class Covert:
    def __init__(self, bit_rate=100., f0=600., f1=900., spl_rate=2000):
        MB = 1024*1024
        self.bit_rate = bit_rate
        self.sym_freqs = (f0, f1)
        self.spl_rate = spl_rate
        self.bufstride = 0.20*MB
        self.bufsize = 16*MB
        self.sync_pattern = np.asarray( 3*[0,1]+[0,1,1,0]+3*[0,1] ) 
        self.test_pkt = np.asarray([0,0,0,1,1,1,0,0])

        # Allocate BW-measure buffer
        self.buf1 = np.ones( (self.bufsize), dtype= np.uint8)
        self.buf2 = np.ones( (self.bufsize), dtype= np.uint8)

    ######################################################################
    # Sending side
    def send_bits(self, arr):
        """
        """
        bufsize = self.bufsize
        bufstride = self.bufstride
        numstrides = bufsize // bufstride
        buf1 = self.buf1
        buf2 = self.buf2

        bit_rate = self.bit_rate
        sym_freqs = self.sym_freqs
        bit_time = 1. / self.bit_rate
        total_time = len(arr) * bit_time

        t0 = time()
        cur_time = 0.
        bufpos = 0
        while cur_time < (total_time):
            cur_bit = int(cur_time // bit_time)

            f = sym_freqs[ arr[cur_bit] ]
            cur_sym = int(2.*cur_time*f) % 2

            if cur_sym == 1:
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
        rate = self.spl_rate
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
    
    def demod(self, S):
        """
            Decode to bitstream
        """
        spl_rate = self.spl_rate
        bit_rate = self.bit_rate
        bit_len  = spl_rate / bit_rate
        f1 = self.sym_freqs[0]
        f2 = self.sym_freqs[1]

        N = len(S)
        t_end = 1. * N / spl_rate

        t = np.linspace(0, t_end, N)
        f1s = np.sin(2*pi*f1*t)
        f1c = np.cos(2*pi*f1*t)

        f2s = np.sin(2*pi*f2*t)
        f2c = np.cos(2*pi*f2*t)

        S1s = S * f1s
        S1c = S * f1c
        S2s = S * f2s
        S2c = S * f2c

        IK = np.ones(bit_len)
        S1s_ = np.convolve(S1s, IK, "same")
        S1c_ = np.convolve(S1c, IK, "same")
        S2s_ = np.convolve(S2s, IK, "same")
        S2c_ = np.convolve(S2c, IK, "same")

        S1 = S1s_**2 + S1c_**2
        S2 = S2s_**2 + S2c_**2

        return S1 < S2

    def decode(self, B):
        bit_len = self.spl_rate / self.bit_rate
        sp = np.repeat(self.sync_pattern, bit_len)
        sp_len = sp.size

        B_  = 2*B - 1
        sp_ = 2*sp - 1

        C = np.correlate(B_, sp_, "same")

        cand = np.where(C > 0.8*sp_len)[0]

        max_pkt_len = 8
        max_pkt_len_ = max_pkt_len * bit_len
        pkts = []
        while len(cand) > 0:
            first = max(0, int(cand[0] - sp_len//2))
            last  = int(cand[0] + sp_len//2)
            pos = first + np.argmax( C[first:last] )
        
            pkt_start = pos + sp_len//2

            P = 1.*B[pkt_start:pkt_start+max_pkt_len_]
            n_bit = int(len(P) / bit_len)
            P = P[:n_bit*bit_len]
            P = P.reshape( (-1, bit_len) )
            pkts.append( np.mean(P, axis=1) )

            #print 70*"-"
            #print first, pos, last, pkt_start
            #print P

            cand = cand[cand > last]

        return pkts

def show_sig(S, rowsize=120):
    rows = int(S.size // rowsize)
    N = rows * rowsize

    S = S[0:N].reshape( (rows, rowsize) )
    pylab.imshow(S, interpolation="nearest")
