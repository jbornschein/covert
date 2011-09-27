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
    return tv.tv_usec;
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


void measure(double usec, double rate, double *bw)
{
    unsigned long buf_size = 256*1024;

    double M = 1000000;
    double G = 1000000000;
    double delta_t = usec*M / rate;

    double cur_usec, last_usec, measured_usec;
    unsigned long offset, last_offset = 0;
    
    struct timespec start_time;
    struct timespec cur_time;

    clock_gettime(DEFAULT_CLOCK, &start_time);
    clock_gettime(DEFAULT_CLOCK, &cur_time);

    cur_usec = ((cur_time.tv_nsec - start_time.tv_nsec) % G) / 1000.;
    last_usec = cur_usec;
    while(cur_usec < usec) {
        
        // Copy and measure
        copy_buf(buf_size)
        cur_usec = ((cur_time.tv_nsec - start_time.tv_nsec) % G) / 1000.;
        measured_usec = cur_usec - last_usec;

        // Store to bw array
        offset = (cur_usec * 1000) / (rate / 1000)
        for (long i=last_offset; i<offset; i++)
            bw[i] =  (double)buf_size / (double)M / (double)measured_usec;

        clock_gettime(DEFAULT_CLOCK, &cur_time);
        last_usec = cur_usec;
    }
}



int main()
{
    double usec = 1000000.;
    double rate = 2000.;

    size_t bw_size = 1000000*usec * rate
    double bw[bw_size];

    measure(usec, rate, bw);

    int i;
    for (i =0: i<bw_size; i++) {
        printf("%f\n", bw[i]);
    }
}

