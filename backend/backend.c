#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>

// #define DEFAULT_CLOCK CLOCK_MONOTONIC // Linux specific
// #define DEFAULT_CLOCK CLOCK_REALTIME
#define DEFAULT_CLOCK 1


typedef long long int v2df __attribute__ ((vector_size (16)));


/**************************************************************
 * Dear MAC OS, clock_gettime is POSIX.
 */

//struct timespec {
//    long tv_sec;
//    long tv_nsec;
//} timespec_t;

unsigned long get_usec() {
    struct timeval tv;

    gettimeofday(&tv, NULL);

    unsigned long usecs = (tv.tv_sec%100)*1000000 + tv.tv_usec;
    return usecs;
}


/**************************************************************/

#define buf_size (16*1024*1024/16)
v2df buf1[buf_size] __attribute__ ((aligned (16)));
v2df buf2[buf_size] __attribute__ ((aligned (16)));


void copy_buf(int nbytes)
{

    register v2df reg;
    static int index = 0;
    int i;
    for (i = 0; i < (nbytes / 16); i++) {
        index = (index + 1) % buf_size;
        //       __builtin_ia32_movntdq(reg, &buf1[index]);
        __builtin_ia32_movntdq(&buf2[index], reg);
    }       
}

const unsigned long M = 1000000;

void measure_c(unsigned long usec, unsigned long rate, unsigned long blk_size, double *bw)
{
    double delta_t = 1. / rate;

    unsigned long start_usec, cur_usec, last_usec, measured_usec;
    unsigned long offset, last_offset = 0;
    

    start_usec = get_usec();
    cur_usec = get_usec() - start_usec;
    while(cur_usec < usec) {

        // Copy and measure
        last_usec = cur_usec;
        copy_buf(blk_size);
        cur_usec = get_usec() - start_usec;
        measured_usec = cur_usec - last_usec;

        // Store to bw array
        offset = ((double)cur_usec/(double)M) / delta_t;
        int i;
        for (i=last_offset; i<offset; i++)
            bw[i] =  ((double)blk_size) / ((double)measured_usec);
        last_offset = offset;

        //printf("%li @ %d: %li, %f\n", cur_usec, offset, measured_usec, bw[i-1]);
    }
}


#ifdef MAIN
int main()
{
    unsigned long usec = 1000000;
    unsigned long rate = 40000;
    unsigned long blk_size = 64*1024;

    size_t bw_size = usec / M * rate;
    double bw[bw_size];

    measure_c(usec, rate, blk_size, bw);

    int i;
    for (i =0; i<bw_size; i++) {
        printf("%f\n", bw[i]);
    }
}

#endif
