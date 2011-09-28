#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>

#define DEFAULT_CLOCK CLOCK_MONOTONIC
#define M 1000000000
typedef long long int v2df __attribute__ ((vector_size (16)));


static inline unsigned long get_nsec()
{
    static struct timespec t;
    clock_gettime(DEFAULT_CLOCK, &t);
    return ( t.tv_sec % 100 ) * M + t.tv_nsec;
}


static inline void copy_buf(int nbytes)
{
    register v2df reg;
    v2df buf[128];
    int i;
    for (i = 0; i < (nbytes / 16); i++) {
        __builtin_ia32_movntdq(&buf[i % 128], reg);
    }       
}


void measure_c(const unsigned long usec, const unsigned long rate, const unsigned long blk_size, double *bw)
{
    double delta_t = 1. / rate;
    unsigned long start_nsec, cur_nsec, last_nsec, measured_nsec;
    unsigned long offset, last_offset = 0;
    unsigned long nsec = usec * 1000;
    start_nsec = get_nsec();
    cur_nsec = get_nsec() - start_nsec;
    while(cur_nsec < nsec) {

        // Copy and measure
        last_nsec = cur_nsec;
        copy_buf(blk_size);
        cur_nsec = get_nsec() - start_nsec;
        measured_nsec = cur_nsec - last_nsec;

        // Store to bw array
        offset = ((double)cur_nsec/(double)M) / delta_t;
        int i;
        for (i=last_offset; i<offset; i++)
            bw[i] =  ((double)blk_size) / ((double)measured_nsec / 1000.);
        last_offset = offset;

        //printf("%li @ %d: %li, %f\n", cur_usec, offset, measured_usec, bw[i-1]);
    }
}

