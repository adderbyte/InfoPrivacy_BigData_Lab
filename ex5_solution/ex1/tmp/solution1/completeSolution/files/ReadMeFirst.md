2) 0x080484d8   : The memory address useful to us: start of where buffer is

1)  break *0x080484d8  : establish break point at this point 


3) set locale: (as root)
locale-gen "en_US.UTF-8"
dpkg-reconfigure locales 


4) 240 bytes causes the fault note this 

5) 


##############################################################################################33

1) disas foo
    ** check where the buffer start 
    >>>> 0x08048471 

2) break * 0x08048476
   *** have a break point here 
   *** then do
   
3) run  $(perl -e 'print "A"x200') 
   *** check the start buffer
   *** This gets A's printed and easy to inspect
   *** When we examine we check for A's (Ox41)

4) x/200xb $esp
   *** inspect or examine the output 
   *** check for where 0x41 starts
   >>>> This is 0xbffff588 -------0xbffff588

5) Go to main. 
   **** disas main
   **** set breakpoint just below disas "call foo"
   **** Observe segmentation fault occurs at 245 bytes;

6) The shell code : is 138 bytes 
 subtract this from 245 
 >>>>>>>>>>>>>>>>>> 245 - 169 = 76


     	
