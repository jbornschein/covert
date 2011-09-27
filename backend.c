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
 * FUCK SHIT MAC OS -- clock_gettime is POSIX you assholes!
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

void copy_buf(int nbytes)
{
    register v2df reg;
    v2df buf[128];

    int i;
    for (i = 0; i < (nbytes / 16); i++) {
        __builtin_ia32_movntdq(&buf[i % 128], reg);
    }       
}

const unsigned long M = 1000000;

void measure_c(unsigned long usec, unsigned long rate, double *bw)
{
    unsigned long buf_size = 256*1024;

    double delta_t = 1. / rate;

    unsigned long start_usec, cur_usec, last_usec, measured_usec;
    unsigned long offset, last_offset = 0;
    

    start_usec = get_usec();
    cur_usec = get_usec() - start_usec;
    while(cur_usec < usec) {
        // Copy and measure
        last_usec = cur_usec;
        copy_buf(buf_size);
        cur_usec = get_usec() - start_usec;
        measured_usec = cur_usec - last_usec;

        // Store to bw array
        offset = ((double)cur_usec/(double)M) / delta_t;
        int i;
        for (i=last_offset; i<offset; i++)
            bw[i] =  (double)buf_size / (double)M / (double)measured_usec;
        last_offset = offset;
    }
}


/*
int main()
{
    double usec = 1000000.;
    double rate = 2000.;

    size_t bw_size = usec / M * rate;
    double bw[bw_size];

    measure(usec, rate, bw);

    int i;
    for (i =0; i<bw_size; i++) {
        printf("%f\n", bw[i]);
    }
}

*/
