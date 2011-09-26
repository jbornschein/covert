#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>

#define DEFAULT_CLOCK CLOCK_MONOTONIC
#define BLOCKLEN (1024 * 8)
extern void WriterSSE2_bypass(void *ptr, unsigned long size, unsigned long loops, unsigned long value);
char *src, *trg;


void print_stats(long unsigned int runtime, long unsigned int count)
{
  printf("  %2.2f GB/s\n", ((count * BLOCKLEN) / (1024.0 * 1024.0)) / (runtime / (1000.0 * 1000.0)));
  printf("  runtime: %.2f µS\n", runtime / 1000.0);
  printf("  xferred: %lu MB\n", (count * BLOCKLEN) / (1024 * 1024));
  printf("  blocks: %lu\n", count);
}


void test_memcpy()
{
  long unsigned int count = 0;
  struct timespec start;
  struct timespec test;

  clock_gettime(DEFAULT_CLOCK, &start); // Works on Linux
  while(23)
  {
    memcpy(src, trg, BLOCKLEN);
    count++;
    clock_gettime(DEFAULT_CLOCK, &test); // Works on Linux
    if(test.tv_nsec - start.tv_nsec > 1000 * 100)
      break;
  }
  
  print_stats(test.tv_nsec - start.tv_nsec, count); 
}


void test_SSE2_bypass()
{
  long unsigned int runtime, count = 0;
  struct timespec start;
  struct timespec test;

  clock_gettime(DEFAULT_CLOCK, &start);
  while(23)
  {
    WriterSSE2_bypass(trg, BLOCKLEN, 8, 0xDEAD);
    count+=8;
    clock_gettime(DEFAULT_CLOCK, &test);
    
    if(test.tv_nsec - start.tv_nsec > 1000 * 100)
      break;
  }
  
  print_stats(test.tv_nsec - start.tv_nsec, count);
}


void test_SSE2_bypass_fixed_size()
{
  long unsigned int runtime, count = 0;
  unsigned int repeat = 3;
  struct timespec start;
  struct timespec test;

  clock_gettime(DEFAULT_CLOCK, &start);
  WriterSSE2_bypass(trg, BLOCKLEN, repeat, 0xDEAD);  
  clock_gettime(DEFAULT_CLOCK, &test);
  
  print_stats(test.tv_nsec - start.tv_nsec, repeat);
}


int main(int argc, char **argv)
{
  src = malloc(BLOCKLEN);
  trg = malloc(BLOCKLEN);
  printf("BLOCKSIZE: %.2f KB\n", BLOCKLEN / 1024.0);
  printf("\nMEMCPY:\n");
  test_memcpy();
  printf("\nSSE2-BYPASS:\n");
  test_SSE2_bypass();
  printf("\nSSE2-BYPASS-FIXED-SIZE:\n");
  test_SSE2_bypass_fixed_size();
  
  return 0;  
}
