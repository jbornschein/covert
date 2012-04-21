#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <sys/time.h>

// #define DEFAULT_CLOCK CLOCK_MONOTONIC // Linux specific
// #define DEFAULT_CLOCK CLOCK_REALTIME
// #define DEFAULT_CLOCK 1


typedef long long int v2df __attribute__ ((vector_size (16)));


/**************************************************************
 * Dear MAC OS, clock_gettime is POSIX.
 * clock_gettime is not implemented on OSX
 */
#ifdef __MACH__

uint64_t get_usec() {
    struct timeval tv;

    gettimeofday(&tv, NULL);

    uint64_t usecs = (tv.tv_sec%10)*1000000 + tv.tv_usec;
    return usecs;
}

#else 

uint64_t get_usec() {
    struct timespec ts;

    clock_gettime(CLOCK_MONOTONIC, &ts);

    uint64_t usecs = (ts.tv_sec%100)*1000000 + ts.tv_nsec / 1000;
    return usecs;
}

#endif


__inline__ uint64_t rdtsc(void) {
    uint32_t lo, hi;
    __asm__ __volatile__ (
    "        xorl %%eax,%%eax \n"
    "        cpuid"      // serialize
    ::: "%rax", "%rbx", "%rcx", "%rdx");
    /* We cannot use "=A", since this would use %rax on x86_64 and return only the lower 32bits of the TSC */
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return (uint64_t)hi << 32 | lo;
}


/**************************************************************/
const uint64_t k = 1024;
const uint64_t M = 1024*1024;


#define SLICE_SIZE 4*1024
#define buf_size (16*1024*1024/16)
v2df buf1[buf_size] __attribute__ ((aligned (16)));

inline void copy_buf(int nbytes)
{
    register v2df reg;
    static int index = 0;
    int n_iter = nbytes / 16;
    int i;

    if ( (index+n_iter) >= buf_size)
        index = 0;

    v2df *ptr = &buf1[index];
    
    for (i = 0; i < n_iter; i+=4) {
        __builtin_ia32_movntdq(ptr++, reg);
        __builtin_ia32_movntdq(ptr++, reg);
        __builtin_ia32_movntdq(ptr++, reg);
        __builtin_ia32_movntdq(ptr++, reg);
    }       
    index += n_iter;
}


double cpnsec = 2.5;

float *test_rdtsc(int N, double dt) {
    uint64_t copied;
    uint64_t c0, c1, c2, c_next;
    uint64_t t0, t1;
    int n;

    float *bw = malloc(N*sizeof(float));
    

    t0 = get_usec();
    c0 = rdtsc();
    for (n=0; n<N; n++) {
        c_next = c0 + (n+1)*dt*cpnsec;

        copied = 0;
        c1 = rdtsc();
        do {
            copy_buf(SLICE_SIZE);
            copied += SLICE_SIZE;
            c2 = rdtsc();
        } while (c2 < c_next);
        //bw[n] =  copied;
        //bw[n] =  (c2-c1) / cpnsec;
        bw[n] = (double)copied / ((c2-c1) / cpnsec);
    }
    c1 = rdtsc();
    t1 = get_usec();

    cpnsec = cpnsec/2 + (c1-c0)/(t1-t0)/2000.;
    return bw;
}



/*

void measure_c(unsigned long usec, unsigned long rate, unsigned long blk_size, double *bw)
{
    double delta_t = 1. / rate;

    unsigned long start_usec, cur_usec, last_usec, measured_usec;
    unsigned long offset, last_offset = 0;
    

    start_usec = get_nsec();
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

*/
#ifdef MAIN
int main()
{
    float *bw;
    int i;

    for (;;) {
        bw = test_rdtsc(512, 100000.);
        printf("cpnsec: %5.2f\n", cpnsec);
        for (i=0; i<20; i++) 
            printf("%6.3f\n", bw[i]);
        free(bw);
    }
/*
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
*/
}

#endif
