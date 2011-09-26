#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>

#define DEFAULT_CLOCK CLOCK_MONOTONIC
#define BLOCKLEN (1024 * 8)
#define BURSTLEN 3
char *src;
extern void WriterSSE2_bypass(void *ptr, unsigned long size, unsigned long loops, unsigned long value);

int main(int argc, char **argv)
{
  char *buf = malloc(BLOCKLEN);
  src = malloc(BLOCKLEN);
  struct timespec start;
  struct timespec test;

  while(23)
  {
    clock_gettime(DEFAULT_CLOCK, &start);
    WriterSSE2_bypass(src, BLOCKLEN, BURSTLEN, 0xDEAD);  
    clock_gettime(DEFAULT_CLOCK, &test);
    printf("%ld\n", test.tv_nsec - start.tv_nsec);
  }
  
  free(buf);
  free(src);
  return 0;  
}
